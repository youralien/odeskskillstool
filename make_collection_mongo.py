#script to read files (each file is a document content in raw json format) from a 
#specified folder and write to a MongoDB collection
#Have mongod.exe and mongo.exe running (in that order) when you execute this code
import os
#using pymongo and json
import pymongo
import json


def cast_value_properly(val):
    """Casts the value belonging to a key in a loaded json
    document properly.

    Values from loaded json sometimes come in a unicode
    format.  These unicode characters, whether they are supposed
    to be integers, floats, strings, or lists of any combination
    of these, need to be casted properly to ensure correct
    representation before loading into the Mongo DB for queries.

    Parameters
    ----------
    val: a unicode string
        the value which should be represented as an integer, float,
        string, or list of a combination of these four.

    Returns
    -------
    new_val: an int, float, str, or list
        the newly casted value to be assigned to the key of the
        document (a dictionary).

    Notes
    -----
    It seems like values that are lists, are usually lists of
    strings (i.e. in the case of skills).  Thus this function
    leaves lists alone, because strings are handled correctly, just
    not numbers.
    """

    try:
        new_val = float(val)
    except TypeError:  # A list (of strings)
        return val
    except ValueError:  # An int or str
        try:
            new_v = int(v)
        except ValueError: # A str
            return val

    return new_val


if __name__ == '__main__':
    # Connection to Mongo DB
    try:
        conn=pymongo.Connection()
        print "Connected successfully!!!"
    except pymongo.errors.ConnectionFailure, e:
        print "Could not connect to MongoDB: %s" % e 
    conn

    datadir = os.path.join(os.path.abspath('.'), 'data/')

    # all files in the data directory
    filenames = os.listdir(datadir)

    # limit it to the first n files
    filenames = filenames[:5]

    # Define my mongoDB database
    db = conn.odesk_files

    # Define my collection where I'll insert my search
    # Get a collection
    collection = db.ryan_collection

    # process each file sequentially
    for fn in filenames:
        with open(datadir + fn,'r') as record:
            data=record.read()
        record.close()

        # cast numbers to integers or floats properly
        doc=json.loads(data)
        for k, v in doc.iteritems():
            doc[k] = cast_value_properly(v)                  

        #insert document into collection
        collection.insert(doc)
