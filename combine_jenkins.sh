python combine_xunit.py archive/edx-platform/reports/bok_choy/xunit.xml reports/a11y/xunit.xml
python combine_xunit.py archive/reports/acceptance/*.xml reports/acceptance/xunit.xml
python combine_xunit.py archive/reports/bok_choy/shard_*/xunit.xml reports/bok_choy/xunit.xml
python combine_xunit.py archive/reports/cms/*/nosetests.xml reports/cms/xunit.xml
python combine_xunit.py archive/reports/common/lib/*/shard_*/nosetests.xml reports/common/xunit.xml
python combine_xunit.py archive/reports/lms/shard_*/nosetests.xml reports/lms/xunit.xml
python combine_xunit.py archive/reports/pavelib/paver_tests/shard_*/nosetests.xml reports/pavelib/xunit.xml
