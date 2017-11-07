import mailbox

mailing_lists = ["kewgardens"]


# Find all the text from each message and store it
# along with the subject and author in Mongo
# potentially check if went through spam filter first
# and also eliminate messages by non-registered users
# Delete messages when done with them
def store_and_delete(mailing_list):
    md = mailbox.Maildir('/home/ubuntu/' + mailing_list + '/Maildir')
    for msg in md:
        pass # extract subject, author, just text (no mime attachments/html)
    return


if __name__ == "__main__":
    for mailing_list in mailing_lists:
        store_and_delete(mailing_list)
