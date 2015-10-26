"""Tool to download all the artifacts from all the Jenkins builds on a PR."""

import os, os.path
import shutil
import zipfile

import click
import scrapy
from scrapy.crawler import CrawlerProcess

FILE_DOWNLOAD_AREA = "downloads"


class UnpackZipFile(object):
    def process_item(self, item, spider):
        for downloaded_file in item['files']:
            path = os.path.join(FILE_DOWNLOAD_AREA, downloaded_file['path'])
            if path.endswith(".zip"):
                with zipfile.ZipFile(path, "r") as z:
                    z.extractall(".")
        return item


class DeleteFile(object):
    def process_item(self, item, spider):
        for downloaded_file in item['files']:
            path = os.path.join(FILE_DOWNLOAD_AREA, downloaded_file['path'])
            os.remove(path)


class ResultsZip(scrapy.Item):
    # These two fields are needed for the FilesPipeline.
    file_urls = scrapy.Field()
    files = scrapy.Field()

class PullRequestSpider(scrapy.Spider):
    name = "pull_request"

    def __init__(self, pr_num, *args, **kwargs):
        super(PullRequestSpider, self).__init__(*args, **kwargs)
        self.pr_num = pr_num

    def start_requests(self):
        return [
            scrapy.Request("https://github.com/edx/edx-platform/pull/{}".format(self.pr_num)),
        ]

    def parse(self, response):
        # Get the build details from GitHub.  They are listed in the HTML three
        # times, so use a set to get them just once.
        build_urls = set()
        build_details = response.xpath('.//a[@class="build-status-details right"]')
        for detail in build_details:
            job_url = detail.xpath("@href").extract()[0]
            build_urls.add(job_url)

        for build_url in build_urls:
            yield scrapy.Request(build_url, self.find_build_artifacts)

    def find_build_artifacts(self, response):
        artifacts_link = response.xpath('.//a[text()="Build Artifacts"]/@href')[0]
        url = response.urljoin(artifacts_link.extract())
        yield scrapy.Request(url, self.download_build_artifacts)

    def download_build_artifacts(self, response):
        for link in response.xpath('.//a'):
            text = link.xpath('text()').extract()
            if not text:
                continue
            text = text[0].strip()
            if text == "(all files in zip)":
                link = response.urljoin(link.xpath('@href').extract()[0])
                print "LINK: %s" % (link,)
                results = ResultsZip(file_urls=[link])
                yield results

@click.command()
@click.option("--debug", is_flag=True)
@click.argument("pr_number", type=int)
def main(debug, pr_number):
    process = CrawlerProcess({
        'FILES_STORE': FILE_DOWNLOAD_AREA,
        'ITEM_PIPELINES': {
            'scrapy.pipelines.files.FilesPipeline': 200,
            '__main__.UnpackZipFile': 300,
            '__main__.DeleteFile': 400,
        },
        'LOG_LEVEL': 'DEBUG' if debug else 'WARNING',
    })

    process.crawl(PullRequestSpider, pr_num=pr_number)
    process.start()

    shutil.rmtree(FILE_DOWNLOAD_AREA)

if __name__ == "__main__":
    main()
