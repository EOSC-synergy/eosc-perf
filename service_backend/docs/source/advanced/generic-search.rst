Generic search
==============
All main request endpoints have the standard API methods List which should
include enough argument options to configure most of your required searches.
However, in those cases where the search is not required to be so strict, 
some endpoints include the `custom method` ``:search``.

Use this method to get a list of items based on a general search
of terms. For example, calling this custom method with ``terms=A``
and ``terms=B`` would return all those endpoint items that contain
a 'A' **and** 'B' on the main json fields (except `id`). For example
in the case of ``\sites:search``, it will return all the sites that
contain an 'A' and a 'B' on the `name`, `address` or `description`
fields. 

As usual, the response returns a pagination object with the filtered
items or the corresponding error code.