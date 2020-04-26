import os
import multiprocessing

NUM_OF_THREADS = 250
FILE_NAME = "."


###############################################
# in this code by using the phenotypes id in the "FILE_NAME".txt file
# and its .fastq files we will make its SNP usinf bwa and samtools
# if the code fail in make SNP of special phenotype, the id will be
# write in the "missIdForSNP.txt"
###############################################

def cloneDirectories():
    cmd = "git clone https://github.com/lh3/bwa.git"
    os.system(cmd)

    cmd = "git clone https://github.com/dcjones/fastq-tools.git"
    os.system(cmd)

    cmd = "git clone https://github.com/samtools/samtools.git"
    os.system(cmd)

    cmd = "git clone https://github.com/samtools/htslib.git"
    os.system(cmd)

    cmd = "git clone https://github.com/samtools/bcftools.git"
    os.system(cmd)

    cmd = "git clone https://github.com/vcftools/vcftools.git"
    os.system(cmd)

    cmd = "git clone https://github.com/broadinstitute/gatk.git"
    os.system(cmd)

    cmd = "cd bwa; make"
    os.system(cmd)

    cmd = "cd hstlib; make"
    os.system(cmd)

    cmd = "cd samtools; make"
    os.system(cmd)

    cmd = "cd bcftools; make"
    os.system(cmd)

    cmd = "cd fastq-tools; ./autogen.sh"
    os.system(cmd)

    cmd = "cd fastq-tools; ./configure && make install"
    os.system(cmd)

    cmd = "cd gatk; ./gradlew bundle"
    os.system(cmd)


# ______________________________________________________
folderContent3 = os.listdir(FILE_NAME)
folderContent = os.listdir(FILE_NAME)
id = []


def getFileNames():
    for i in range(0, len(folderContent)):
        if folderContent[i].__contains__("_1.fastq") and folderContent[i].__contains__("ERR") and (
                not folderContent[i].__contains__("fastq.gz")):  # TODO
            id.append(folderContent[i][:len(folderContent[i]) - 8])  # - 11])


def sleepMode(id, sleepNow):
    if not sleepNow:
        print("start sleeeeeeeeeeeeeeeep for " + id)
        import time
        time.sleep(1800)
        print("finish sleeeeeeeeeeeeeeeep for " + id)
        samToolsSNP(id, True)
    else:
        with open("missIdForSNP.txt", "a+") as txt_file:
            txt_file.write(id + '\n')
        print("was't able to make SNP data for : " + id)


def samToolsSNP(id, sleepNow=False):
    print("start SNP process for :" + id)
    try:
        fileName1 = id + "_1.fastq"
        fileName2 = id + "_2.fastq"

        secondFileExist = False
        for i in range(0, len(folderContent)):
            if folderContent[i].__contains__(id + "_2.fastq"):
                secondFileExist = True
                cmd2 = "cd bwa; ./bwa mem -M -R '@RG\\tID:sample_1\\tLB:sample_1\\tPL:ILLUMINA\\tPM:HISEQ\\tSM:sample_1' " \
                       "../ref.fna ../" + fileName1 + " ../" + fileName2 + " > ../" + id + ".sam "
                break
        if not secondFileExist:
            cmd2 = "cd bwa; ./bwa mem -M -R '@RG\\tID:sample_1\\tLB:sample_1\\tPL:ILLUMINA\\tPM:HISEQ\\tSM:sample_1' " \
                   "../ref.fna ../" + fileName1 + " > ../" + id + ".sam "
        cmd3 = "cd samtools; ./samtools view -S -b ../" + id + ".sam > ../" + id + ".bam"
        cmd4 = "cd samtools; ./samtools sort ../" + id + ".bam -o ../my-sorted" + id + ".bam"  # TODO
        cmd5 = "cd samtools; ./samtools faidx ../ref.fna"
        cmd10 = "cd bcftools; ./bcftools mpileup -Ou -f ../ref.fna ../my-sorted" + id + ".bam  | ./bcftools call -mv " \
                                                                                        "-Ov > ../" + id + ".vcf "

        os.system(cmd2)
        os.system(cmd3)
        os.system(cmd4)
        os.system(cmd10)

        print("finshed: " + id)

    except:
        sleepMode(id, sleepNow)


def GATKSNP(id, sleepNow=False):
    a = 1
    print("start SNP process for :" + id)
    try:
        fileName1 = id + "_1.fastq"
        fileName2 = id + "_2.fastq"

        secondFileExist = False
        for i in range(0, len(folderContent)):
            if folderContent[i].__contains__(id + "_2.fastq"):
                secondFileExist = True
                cmd2 = "cd bwa; ./bwa mem -M -R '@RG\\tID:sample_1\\tLB:sample_1\\tPL:ILLUMINA\\tPM:HISEQ\\tSM:sample_1' " \
                       "../ref.fna ../" + fileName1 + " ../" + fileName2 + " > ../" + id + ".sam "
                break

        if secondFileExist == False:
            cmd2 = "cd bwa; ./bwa mem -M -R '@RG\\tID:sample_1\\tLB:sample_1\\tPL:ILLUMINA\\tPM:HISEQ\\tSM:sample_1' " \
                   "../ref.fna ../" + fileName1 + " ../" + fileName2 + " > ../" + id + ".sam "
        cmd3 = "cd gatk; java -jar $EBROOTPICARD/picard.jar SortSam INPUT=../" + id + ".sam OUTPUT=../" + id + ".bam SORT_ORDER=coordinate"
        cmd4 = "cd gatk; java -jar $EBROOTPICARD/picard.jar MarkDuplicates INPUT=../" + id + ".bam OUTPUT=../dedup_reads" + id \
               + ".bam METRICS_FILE=../metrics" + id + ".txt"
        cmd5 = "cd gatk; java -jar $EBROOTPICARD/picard.jar BuildBamIndex INPUT=../dedup_reads" + id + ".bam"
        cmd6 = "cd gatk; java -jar $EBROOTGATK/GenomeAnalysisTK.jar -T RealignerTargetCreator -R ../ref.fna -I ../dedup_reads" + id \
               + ".bam -o ../realignment_targets" + id + ".list"
        cmd7 = "cd gatk; java -jar $EBROOTGATK/GenomeAnalysisTK.jar -T IndelRealigner -R ../ref.fna -I ../dedup_reads" + id \
               + ".bam -targetIntervals ../realignment_targets" + id + ".list -o ../realigned_reads" + id + ".bam"
        cmd8 = "cd gatk; java -jar $EBROOTGATK/GenomeAnalysisTK.jar -T HaplotypeCaller -R ../ref.fna -I ../realigned_reads" + id \
               + ".bam -o ../" + id + "_GATK.vcf"

        os.system(cmd2)
        os.system(cmd3)
        os.system(cmd4)
        os.system(cmd5)
        os.system(cmd6)
        os.system(cmd7)
        os.system(cmd8)

        print("finshed: " + id)

    except:
        sleepMode(id, sleepNow)


###############################################
# 1- vcf_to_tsv
#
# Convert the vcf into a csv by deleting the lines that start with ##
#
# 2- Creating SNP_table
#
# 3- Find and store gene sequences in isolates
###############################################

def preprocessing(id):
    # Part one
    f_in = open(id + ".vcf", 'r')
    f_out = open(id + ".csv", 'w')
    for line in f_in:
        if line.startswith("##"):
            continue
        f_out.write(line)

    f_in.close()
    f_out.close()

    # Part two
    INPUT_FILE = id + ".csv"
    OUTPUT_FILE = id + "_table.csv"

    import pandas as pd
    import numpy as np

    xx = pd.read_csv(INPUT_FILE, sep='\t', header=0)
    xx['INFO'] = xx['INFO'].str.split(';').str[-2].str.split('=').str[-1]
    df = xx.copy()
    # print df
    df.drop(['#CHROM', 'ID', 'FILTER', 'FORMAT'], inplace=True, axis=1)

    multi_variants_ind = np.where(df['ALT'].str.contains(',') & df['INFO'].str.contains(','))[0]
    multi_variants_df = df.iloc[multi_variants_ind.tolist(),]

    # print multi_variants_df
    if len(multi_variants_ind) != 0:
        new_multi_df = (
            multi_variants_df.set_index(multi_variants_df.columns.drop(['ALT'], 1).tolist()).ALT.str.split(',',
                                                                                                           expand=True).stack().reset_index().rename(
                columns={0: 'ALT'}).loc[:, multi_variants_df.columns])
        print("____")
        print(new_multi_df)
        new_multi_df.drop([0], axis=0,
                          inplace=True)  # in case of multi snp in one position we just keep the simplest one
        df.drop(multi_variants_ind.tolist(), axis=0, inplace=True)

        df = df.append(new_multi_df)

    df.drop(['QUAL', 'INFO'], inplace=True, axis=1)

    df.to_csv(OUTPUT_FILE, index=False, mode='w', header=True)


def commonVarients(id):
    FILE_NAME1 = "../" + id + ".vcf"
    FILE_NAME2 = "../" + id + "_GATK.vcf"

    folderContent2 = os.listdir(FILE_NAME)

    appear = False
    for i in range(0, len(folderContent2)):
        if folderContent2[i].__contains__(id + "_GATK.vcf"):
            appear = True
            break
    if not appear:
        os.system("mv " + id + ".vcf" + " Final_" + id + ".vcf")
        return

    os.system("cd bcftools; ./bcftools view " + FILE_NAME1 + " -Oz -o " + FILE_NAME1 + ".gz")
    os.system("cd bcftools; ./bcftools index " + FILE_NAME1 + ".gz")
    os.system("cd bcftools; ./bcftools view " + FILE_NAME2 + " -Oz -o " + FILE_NAME2 + ".gz")
    os.system("cd bcftools; ./bcftools index " + FILE_NAME2 + ".gz")
    os.system("mkdir " + id)
    os.system("cd bcftools; ./bcftools isec " + FILE_NAME1 + ".gz " + FILE_NAME2 + ".gz -p ../" + id)
    os.system("mv " + id + "/0002.vcf Final_" + id + ".vcf")


def pipeLine(id):
    fileName1 = id + "_1.fastq"
    fileName2 = id + "_2.fastq"

    for i in range(0, len(folderContent3)):
        if folderContent3[i].__contains__(id + "_table.csv"):
            print(id + " Exist")
            return

    samToolsSNP(id)
    GATKSNP(id)
    commonVarients(id)
    preprocessing("Final_" + id)
    os.system("rm -rf " + fileName2)
    os.system("rm -rf " + fileName1)


def main():
    # run this part only at first run!\
    cloneDirectories()

    getFileNames()
    pool = multiprocessing.Pool(processes=NUM_OF_THREADS)
    pool.map(pipeLine, (id[i] for i in range(0, len(id))))


main()
