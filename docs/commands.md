# GRE2G Commands

*GRE2G is conntrolled by executing runtime script* `gre2g_run.py` *with commandline arguments variants.*
The commands overview is divided into theme sections for easier understanding.

## Management Commands

### Init
Initializes GRE2G's underlying strcutures - e.g. creates databases. If the structures already exists, it deletes those
and creates new ones.

##### :bulb: Cmd Template :point_down:

``` bash
python gre2g_run.py \
    settings.temp_path=<TEMP_FOLDER_PATH> \
    settings.blob_database.database_path=<BLOB_DATABSE_FOLDER_PATH> \
    run=init \
    hydra.run.dir=.
```
