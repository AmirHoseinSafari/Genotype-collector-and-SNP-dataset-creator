import os
import multiprocessing

NUM_OF_THREADS = 1
FILE_NAME = "/Users/amir/PycharmProjects/Lab/phenotypeCollector"

###############################################
# in this code by using the phenotypes id in the "FILE_NAME".txt file
# and its .fastq files we will make its SNP usinf bwa and samtools
# if the code fail in make SNP of special phenotype, the id will be
# write in the "missIdForSNP.txt"
###############################################

# run this part only at first run!
print "Clone required repos"
cmd = "git clone https://github.com/lh3/bwa.git"
os.system(cmd)

cmd = "git clone https://github.com/samtools/samtools.git"
os.system(cmd)

cmd = "git clone https://github.com/samtools/htslib.git"
os.system(cmd)

cmd = "git clone https://github.com/samtools/bcftools.git"
os.system(cmd)

cmd = "git clone https://github.com/vcftools/vcftools.git"
os.system(cmd)

cmd = "cd bwa; make"
os.system(cmd)

cmd = "cd hstlib; make"
os.system(cmd)

cmd = "cd samtools; make"
os.system(cmd)

cmd = "cd bcftools; make"
os.system(cmd)


#______________________________________________________

folderContent = os.listdir(FILE_NAME)
id = []

for i in range(0, len(folderContent)):
    if folderContent[i].__contains__("_1.fastq.gz"):
        id.append(folderContent[i])


def samToolsSNP(id, sleepNow=False):
    print "start SNP process for :" + id
    try:
        fileName1 = id + "_1.fastq"
        fileName2 = id + "_2.fastq"

        cmd01 = "gunzip " + fileName1 + ".gz"
        cmd02 = "gunzip " + fileName2 + ".gz"

        os.system(cmd01)
        os.system(cmd02)

        cmd1 = "cd bwa; ./bwa index ../ref.fna"
        cmd2 = "cd bwa; ./bwa aln ../ref.fna ../" + fileName1 + " ../" + fileName2 + " > " + id + ".sai"
        cmd25 = "cd bwa; ./bwa samse ../ref.fna " + id + ".sai ../" + fileName1 + " ../" + fileName2 + " > ../" + id + ".sam"
        cmd3 = "cd samtools; ./samtools view -S -b ../" + id + ".sam > ../" + id + ".bam"
        cmd4 = "cd samtools; ./samtools sort ../" + id + ".bam -o ../my-sorted" + id + ".bam" # TODO
        cmd5 = "cd samtools; ./samtools faidx ../ref.fna"
        cmd10 = "cd bcftools; ./bcftools mpileup -Ou -f ../ref.fna ../my-sorted" + id + ".bam  | ./bcftools call -mv -Ov > ../SNP/" + id + ".vcf"

        os.system(cmd1)
        os.system(cmd2)
        os.system(cmd25)
        os.system(cmd3)
        os.system(cmd4)
        os.system(cmd5)
        os.system(cmd10)

        print "finshed: " + id

        cmd20 = "rm " + fileName1
        cmd21 = "rm " + fileName2
        cmd22 = "rm " + id + ".sai"
        cmd23 = "rm " + id + ".sam"
        cmd24 = "rm " + id + ".bam"
        cmd25 = "rm my-sorted" + id + ".bam"

        os.system(cmd20)
        os.system(cmd21)
        os.system(cmd22)
        os.system(cmd23)
        os.system(cmd24)
        os.system(cmd25)

        print "delete files: " + id
    except:
        if sleepNow == False:
            print "start sleeeeeeeeeeeeeeeep for " + id
            import time
            time.sleep(1800)
            print "finish sleeeeeeeeeeeeeeeep for " + id
            samToolsSNP(id, True)
        else:
            with open("missIdForSNP.txt", "a+") as txt_file:
                txt_file.write(id + '\n')
            print "was't able to make SNP data for : " + id


def main():
    pool = multiprocessing.Pool(processes=NUM_OF_THREADS)
    pool.map (samToolsSNP, (id[i] for i in range(0, len(id))))

main()
