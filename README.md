# isa-json2tab
simple stateless backend to convert ISA-JSON to ISA-Tab implemented in [bottle](http://bottlepy.org/docs/dev/index.html) and using the [isa-api](https://github.com/ISA-tools/isa-api) for conversion.

## Usage
Send your ISA-JSON via HTTP `POST` to `<hostname>/json2tab` in the request body, the server will respond with `application/zip` content containing a ZIP archive of the generated ISA-Tab files.
An example implementation using this service can be seen in the [MIAPPE Wizard repo](https://github.com/IPK-BIT/miappe-wizard/blob/main/src/lib/getIsaTab.js).

## Container
The backend is available as a Docker Image from https://hub.docker.com/r/thyra/isa-json2tab .
