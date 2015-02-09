# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Bill Wong

"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons, aa_table
import random
from load import load_seq

def shuffle_string(s):
    """ Shuffles the characters in the input string
        NOTE: this is a helper function, you do not have to modify this in any way """
    return ''.join(random.sample(s,len(s)))

### YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###


def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'

    Check G
    >>> get_complement('G')
    'C'

    Check T
    >>> get_complement('T')
    'A'
    """

    if nucleotide == 'A':
        return 'T'
    if nucleotide == 'C':
        return 'G'
    if nucleotide == 'G':
        return 'C'
    if nucleotide == 'T':
        return 'A'

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'

    Unit tests are sufficient because it tests everything.
    """

    rev = dna[::-1]
    res = ''
    for i in rev:
        res = res + get_complement(i)
    return res

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'

    Test with no stop codon:
    >>> rest_of_ORF('ATGGGAGGA')
    'ATGGGAGGA'

    Test with out-of-frame stop codon:
    >>> rest_of_ORF('ATGGTAG')
    'ATGGTAG'
    """
    # TODO: implement this
    for i in range(0,len(dna),3):   # search in threes
        if dna[i:i+3] in codons[10]:    # check for a stop codon
            return dna[:i]
    return dna[:]

def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']

    Test with one ORF:
    >>> find_all_ORFs_oneframe("ATGAAATAG")
    ['ATGAAA']

    Test with nested ORFs:
    >>> find_all_ORFs_oneframe("AAAATGATGAAATAG")
    ['ATGATGAAA']

    Test with out-of-frame ORFs:
    >>> find_all_ORFs_oneframe("AATGAAATAG")
    []
    """
    res = []
    i = 0
    while i < len(dna):
        if dna[i:i+3] in codons[3]:    # check for a start codon
            this_ORF = rest_of_ORF(dna[i:])
            res.append(this_ORF)
            i += len(this_ORF)  # skip past this ORF
        i += 3  # check the next three
    return res

def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    
    Test for nested ORFs:
    >>> find_all_ORFs('ATGATGAAATAG')
    ['ATGATGAAA']
    """
    # TODO: implement this
    res = find_all_ORFs_oneframe(dna)
    res = res + find_all_ORFs_oneframe(dna[1:]) # shifted over one base
    res = res + find_all_ORFs_oneframe(dna[2:]) # shifted over two bases
    return res

def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']

    Doctest is sufficient, tests on both strands
    """
    # TODO: implement this
    res = find_all_ORFs(dna)
    res = res + find_all_ORFs(get_reverse_complement(dna))
    return res

def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'

    Doctest is sufficient, tests for longest ORF

    Test for two ORFs or same size: (uses the first ORF it finds)
    >>> longest_ORF("ATGAAATAGATGTTTTAG")
    'ATGAAA'
    """
    all_ORFs = find_all_ORFs_both_strands(dna)
    if all_ORFs == []:
        return [] # if there are no ORFs, return an empty list
    return max(all_ORFs, key = len)

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence

        If there are no ORFs, it returns ['']
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    all_ORFs = ['']
    for i in range(num_trials): # repeat num_trials times
        this_ORF = shuffle_string(dna)  # shuffle the string
        all_ORFs.append(longest_ORF(this_ORF))  # adds the longest ORF it found to all_ORFs list
    longest = max(all_ORFs, key = len)  # find the longest ORF in all_ORFs
    return len(longest)    # return the length of the longest ORF

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'

        Doctest is sufficient, tests for when len(dna) is not divisible by three
    """
    res = ''
    stop = len(dna) - (len(dna) % 3)    # ignore the last codon if it's less than 3 bases long
    for i in range(0,stop,3):   # search in threes
        res += aa_table[dna[i:i+3]] # add the amino acid from the dictionary to the result
    return res

def gene_finder(dna):
    """ Returns the amino acid sequences that are likely coded by the specified dna
        
        dna: a DNA sequence
        returns: a list of all amino acid sequences coded by the sequence dna.
    """
    threshold = longest_ORF_noncoding(dna,1500) # find the theshold
    all_ORFs = find_all_ORFs_both_strands(dna)  # find all ORFs
    above_threshold_aas = []

    for e in all_ORFs:  # step through every element of all_ORFs
        if len(e) > threshold: # if the length of this element is above the theshold 
            aa_chain = coding_strand_to_AA(e)   # convert the element to amino acids
            above_threshold_aas.append(aa_chain)   # add it to the above_threshold amino acids list
    return above_threshold_aas

dna = load_seq("./data/X73525.fa")
print gene_finder(dna)

if __name__ == "__main__":
    import doctest
    doctest.testmod()