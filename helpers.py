import vobject
import csv
import os


def _parseName(fullname: str) -> str:
    # this function assumes people have one first name without whitespace, when spelled out
    # and all other words in a person's name are part of their last name
    names = fullname.split()

    names[1:-1] = [n.lower() for n in names[1:-1]]
    names[-1] = names[-1].capitalize()
    lname = str.join(" ", names[1:])
    fname = names[0].capitalize()

    return fname, lname


def _parseNumber(number: str) -> str:
    # this function can only handle Dutch numbers starting with '06' and having 10 digits in total
    number = str.join("", number.split())
    if len(number) == 10:
        number = "+31" + number[1:]
    return number


def importContacts(file_loc: str) -> list[tuple]:
    with open(file_loc) as file:
        contacts = list(csv.reader(file))
    contacts = [c[0].split(";") for c in contacts]
    contacts = [
        [_parseName(name) for name in [x[0] for x in contacts]],
        [_parseNumber(number) for number in [x[1] for x in contacts]],
    ]  # [[names], [numbers]]
    contacts = list(
        zip(*contacts)
    )  # transpose the lists to get tuples of (name, number)

    return contacts


def convertOne(
    fname: str, lname: str, number: str, suffix: str = "YouChooze"
) -> vobject:
    vc = vobject.vCard()
    vc.add("n")
    vc.n.value = vobject.vcard.Name(given=fname, family=lname, suffix=suffix)
    vc.add("fn")
    vc.fn.value = fname + " " + lname
    vc.add("tel")
    vc.tel.value = number

    return vc


def toVCard(cs: list) -> list:
    return [
        convertOne(c[0][0], c[0][1], c[1], suffix="YouChooze") for c in cs if c[1]
    ]  # convert to vCard, if number is given


def writeVCFs(vcards: list, dir: str = "./output/") -> None:
    if not os.path.exists(dir):
        os.mkdir(dir)
    for contact in vcards:
        filename = str.join("_", contact.contents["fn"][0].value.split()) + ".vcf"
        with open(dir + filename, "w") as vcf:
            vcf.write(contact.serialize())
