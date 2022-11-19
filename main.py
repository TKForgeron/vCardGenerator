from helpers import importContacts, toVCard, writeVCFs

"""
This is an example

Line 1: Give a location of a two-column (name, number) csv file 
Line 2: Converts the list of tuples ( ((first name, last name), number) ) to a list of vCards
Line 3: Writes these vCards to a given location (in `.vcf` format)
"""


contacts = importContacts("data/yc_contacts.csv")
vCards = toVCard(contacts)
writeVCFs(vCards, "./output/")
