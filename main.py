from helpers import importContacts, toVCard, writeVCFs

contacts = importContacts("data/yc_contacts.csv")
vCards = toVCard(contacts)
writeVCFs(vCards)
