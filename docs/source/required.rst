.. _Required tools or databases:

Required tools or databases
===========================

Each module has different required tools or databases. **For running a module, the 
users just need to install the specific tools for it.** For examples, running 
TSS prediction only needs TSSpredator.

Please also check our `Docker image <https://hub.docker.com/r/silasysh/annogesic/>`_.
Via Docker image, all the required tools are installed.

Tools
-----

`Python <https://www.python.org/>`_ : version higher or equal to 3.4.

`BioPython <http://biopython.org/wiki/Main_Page>`_: version higher or equal to 1.65.

`BioPerl <http://www.bioperl.org/wiki/Main_Page>`_:  version higher or equal to 1.6.1.

`Wget <https://www.gnu.org/software/wget>`_:  version higher or equal to 1.17.1.

`Blast+ <ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/>`_ : version higher or equal to 2.2.28+ (for sRNA_detection).

`ImageMagick <http://www.imagemagick.org/script/index.php>`_ : version higher or equal to 6.9.0-0 (for generate screenshot).

`Infernal <http://infernal.janelia.org/>`_ : version higher or equal o 1.1.1 (for riboswitch and RNA thermometer detection).

`Matplotlib <http://matplotlib.org/>`_ : version higher or equal to 1.5.0 (for generate all statistics figure).

`Networkx <https://networkx.github.io/>`_ : version higher or equal to 1.10 (for generate PPI figure).

`MEME <http://meme-suite.org/tools/meme>`_ : version higher or equal to 4.11.1 (for promoter detection).

`GLAM2 <http://meme-suite.org/tools/glam2>`_ : version higher or equal to 4.11.1 (for promoter detection).

`MPICH <http://www.mpich.org/>`_ : version higher or equal to 3.2 (for parallel version of promoter detection).

`RATT <http://www.sanger.ac.uk/resources/software/pagit/>`_ : version higher or equal to 1.64 (for annotation transfer).
Please be attention, before you start to run RATT (annotation transfer), run ``source $PAGIT_HOME/sourceme.pagit`` first. It will
modify the path for execute RATT. If you run ANNOgesic through Docker container, you can skip this step.

`Psortb <http://www.psort.org/psortb/>`_ : version higher or equal to 3.0 (for subcellular localization detection).

`Samtools <https://github.com/samtools>`_ : version higher or equal to 1.3.1 (using htslib 1.3.1) (for SNP calling, CircRNA_detection).

`Bcftools <https://github.com/samtools>`_ : version higher or equal to 1.3.1 (using htslib 1.3.1) (for SNP calling).

`Segemehl <http://www.bioinf.uni-leipzig.de/Software/segemehl/>`_ : version higher or equal to 0.1.9 (for CircRNA_detection).
When you install Segemehl, please type 'make all' instead of 'make' after running configure. Otherwise, the testrealign.x won't appear. 

`TranstermHP <http://transterm.cbcb.umd.edu/>`_ : version higher or equal to 2.09 (for rho-independent terminator prediction).

`TSSpredator <http://it.inf.uni-tuebingen.de/?page_id=190>`_ : version higher or equal to 1.06 (for TSS and processing site prediction, TSS optimization).

`ViennaRNA <http://www.tbi.univie.ac.at/RNA/>`_ : version higher or equal to 2.3.2 (for rho-independent terminator prediction, sRNA detection, sRNA_target detection).
ViennaRNA contains RNAfold, RNAup, RNAplex, RNAplfold, mountain.pl, relplot.pl for executing many modules of ANNOgesic.

`IntaRNA <https://github.com/BackofenLab/IntaRNA/>`_: version higher or equal to 2.0.4 (sRNA_target detection) 

`IGV <https://www.broadinstitute.org/software/igv/home>`_ (for screenshot and color_png).

`CRT <http://www.room220.com/crt/>`_: version higher or equal to 1.2 (for CRISPR detection).

Databases
---------

`BSRD <http://www.bac-srna.org/BSRD/index.jsp>`_ (for sRNA detection)

`nr database <ftp://ftp.ncbi.nih.gov/blast/db/FASTA/>`_ (for sRNA detection)

`Rfam <http://rfam.xfam.org/>`_ (for riboswitch and RNA thermometer detection)

`idmapping_selected.tab from Uniprot <http://www.uniprot.org/downloads>`_ (for Go term detection)

`goslim.obo <http://geneontology.org/page/go-slim-and-subset-guide>`_ (for Go term detection)

`go.obo <http://geneontology.org/page/download-ontology>`_ (for Go term detection)

`species.v${VERSION}.txt from STRING
<http://string-db.org/cgi/download.pl>`_ (for protein-protein
interaction prediction; replace ${VERSION} by the version you would
like to use)
