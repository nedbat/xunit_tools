===============
XUnit.xml Tools
===============

To get edx-platform results for a pull request:

#. pip install -r requirements.pip

#. python download_jenkins_results.py PR_NUMBER

   This pulls down all of the artifacts into an archive/ directory.

#. ./combine_jenkins.sh

   This combines xunit.xml files into pieces we can understand. Shards on
   Jenkins need to be recombined.

#. python htmlwriter.py reports > results.html
    
   This makes an HTML page from the combined results.
