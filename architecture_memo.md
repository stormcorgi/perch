# architecture memo

## domain

* Folder
  * Actress
  * Author
* Item
  * Movie
  * Book
* TagGroup
* Tag

## repository implements

* Memory(for testing)
* RawJson(for testing, terrible performance)
* SQLAlchemy(for production, good performance, handle SQLite)

## usecase

every usecase handle datas on Repos.
actual read/write data is done by repos functionality.

* Folder
  * List entire folders
  * Search
    * by name
    * by id
  * ~~Add~~ (it should be depend on Eagle)
  * ~~Delete~~ (it should be depend on Eagle)

* Item
  * List entire Items
  * List Folders(an item can be belong on several folders at same time)
  * Search
    * by file name
    * by id
  * ~~Add~~ (it should be depend on Eagle)
  * ~~Delete~~ (it should be depend on Eagle)
  * Add into Folder
  * Remove from Folder
  * Add existing tag
  * Remove existing tag
  * Change Rate

* TagGroup
  * List entire TagGroup
  * Search
    * by name
  * Add itself
  * Delete itself

* Tag
  * Add
  * Delete
  * Add into Group
  * Remove from Group

* Repo
  * Update Repo
    * Find difference current repo and actual environment data(json)
      * Add/Delete/Update Folder
      * Add/Delete/Update Item
      * Add/Delete/Update TagGroup
      * Add/Delete/Update Tag
  * Drop Repo

* Others
  * Random item