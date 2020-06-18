# gostep
Serverless Templates Provider for Google cloud platform.

### Prerequisites

* [python v3.x](https://www.python.org/downloads/)
* [Subversion CLI](https://subversion.apache.org/packages.html)
* [gcloud SDK](https://cloud.google.com/sdk)


### How to install

#### From PyPI
```bash
pip install gostep
```

#### From source
Simply clone the repository or download source.
```bash
cd gostep
python setup install
```

### Commands reference

```bash
gostep ---|
          | auth ------|---------- init ---| <service_account_name> ---|
          |------------|-------------------|---------------------------| inside ------------| <workspace_dir>
          |------------|-------------------|---------------------------| diplayname --------| <account_diplayname>
          |------------|---------- show ---|---------------- inside ---| <workspace_dir>
          |
          | base ------|---------- init ---|--- <your_project_name> ---|
          |------------|-------------------|---------------------------| location ----------| <gcloud_location_id>
          |------------|-------------------|---------------------------| inside ------------| <workspace_dir>
          |------------|-------------------|---------------------------| verison -----------| <yourr_project_version>
          |------------|-------------------|---------------------------| explains ----------| <description>
          |
          | service ---|---------- init ---|- <cloud_function_name> ---| inside ------------| <workspace_dir>
          |------------|-------------------|---------------------------| location ----------| <gcloud_location_id>
          |------------|-------------------|---------------------------| env ---------------| <runtime_environment> 
          |------------|-------------------|---------------------------| explains ----------| <description>
          |------------| 
          | deploy ----| 'diff'
          |------------| <service_name> ---|
          |------------|-------------------|---------------- inside ---| <workspace_dir>
          |------------|-------------------|-------------- location ---| <gcloud_location_id>
          |
          | gcloud ----| projects
          |------------| locations

