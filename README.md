# Introduction
This repository is a group of wrappers for different services and technologies. To keep it simple, this wrapper are some Python methods for interacting with the British Library resources.

Current available and working functionality:

- Metadata extractor from a book search.
- Book merger from images resources from the British Library.

# Functionalities
Right now, you can get all the metadata of any book from a search using "metadata_extractor" method and changing the keywords from the variables file. This might be useful in order to extract some statistics about a bunch of entries: language distribution, author productivity, UIN, etc.


Also you can merge all the images from a book if you have the ark_id and vdc_id. This is easy to get:

- First, look for the book in images you want to have.
- Second, look to the url and you will see something like "https://api.bl.uk/metadata/iiif/ark:/*****/*****x000...'
- From the URL you can get the ark_id which is the number after the "ark:" text and the vdc_id which is the code afterwards. You can see on the variables file an example which you must change to get the book you want.

You must know that this method is quicker than asking for the official service to download it.


## Next Steps
A new method for extract all the images from a search is on the way. It will make much more easy to download a huge volume of images at once.

If you have any feedback or suggestion for new functionalities on this wrapper, I am glad to hear about.

### Disclaimer
This is not an official wrapper by any means but an attemp to approach this resource to more people.
