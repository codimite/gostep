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
```

## License
MIT License
Copyright (c) 2018 Lahiru Pathirage and Codimite pvt ltd.
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "gostep"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.