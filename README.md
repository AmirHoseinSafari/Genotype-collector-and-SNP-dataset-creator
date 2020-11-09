# genotypeCollector
Collecting Genotypes from ENA and make their SNPs

## dataCollector.py
In this code by using the Genotypes id in the "FILE_NAME".txt file we will download its .fastq files from ENA databese

## SNP.py
In this code by using the Genotypes id in the "FILE_NAME".txt file and its .fastq files we will make its SNP using bwa and samtools and GATK and get the common SNP of both files and store in ("Final_" + id + ".vcf")

If the code fail in make SNP of special Genotype, the id will be write in the "missIdForSNP.txt"

By calling preprocessing() function you will get the ( "Final_" + id + "_table.csv" ) file which contatin "pos, ref, alt" for each SNP

## tableCreatorGit.py
In this code we make a table for all the isolates

## sparseMatrix.py
Will store the table of tableCreatorGit.py in the sparse format to reduce size

## Citation
If you found the content of this repository useful, please cite us:

https://www.biorxiv.org/content/10.1101/2020.11.07.372136v1?rss=1

@article {Safari2020.11.07.372136,
	author = {Safari, Amir Hosein and Sedaghat, Nafiseh and Forna, Alpha and Zabeti, Hooman and Chindelevitch, Leonid and Libbrecht, Maxwell},
	title = {Predicting drug resistance in M. tuberculosis using a Long-term Recurrent Convolutional Networks architecture},
	elocation-id = {2020.11.07.372136},
	year = {2020},
	doi = {10.1101/2020.11.07.372136},
	publisher = {Cold Spring Harbor Laboratory},
	abstract = {Drug resistance in Mycobacterium tuberculosis (MTB) may soon be a leading worldwide cause of death. One way to mitigate the risk of drug resistance is through methods that predict drug resistance in MTB using whole-genome sequencing (WGS) data. Existing machine learning methods for this task featurize the WGS data from a given bacterial isolate by defining one input feature per SNP. Here, we introduce a gene-centric method for predicting drug resistance in TB. We define one feature per gene according to the number of mutations in that gene in a given isolate. This representation greatly decreases the number of model parameters. We further propose a model that considers both gene order through a Long-term Recurrent Convolutional Network (LRCN) architecture, which combines convolutional and recurrent layers. We find that using these strategies yields a substantial, statistically-significant improvement over the state-of-the-art and that this improvement is driven by the order of genes in the genome and their organization into operons.Competing Interest StatementThe authors have declared no competing interest.},
	URL = {https://www.biorxiv.org/content/early/2020/11/08/2020.11.07.372136},
	eprint = {https://www.biorxiv.org/content/early/2020/11/08/2020.11.07.372136.full.pdf},
	journal = {bioRxiv}
}
