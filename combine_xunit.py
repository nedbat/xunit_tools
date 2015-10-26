"""Combine a number of xunit.xml files into one."""

import click
from lxml import etree

from xunit import TestResults


@click.command()
@click.argument('input_files', nargs=-1, type=click.Path(exists=True))
@click.argument('output_file', nargs=1, type=click.Path())
def main(input_files, output_file):
    out_suite = etree.fromstring("<testsuite></testsuite>")
    tree = etree.ElementTree(out_suite)

    totals = TestResults()

    for input_file in input_files:
        with open(input_file) as in_xml:
            in_tree = etree.parse(in_xml)
        for testsuite in in_tree.xpath("/testsuite"):
            totals += TestResults.from_element(testsuite)
            for testcase in testsuite.xpath("testcase"):
                out_suite.append(testcase)

    totals.onto_element(out_suite)

    with open(output_file, "w") as out_xml:
        out_xml.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="utf8"))


if __name__ == "__main__":
    main()
