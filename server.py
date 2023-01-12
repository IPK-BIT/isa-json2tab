from bottle import route, run, template, response, request, hook, HTTPResponse
from isatools.convert import json2isatab
from tempfile import mkdtemp
from shutil import rmtree, make_archive
from os import mkdir


cors_headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Access-Control-Allow-Headers, Origin, Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers'
}


@hook('before_request')
def handle_options():
    if request.method == 'OPTIONS':
        # Bypass request routing and immediately return a response
        raise HTTPResponse(headers=cors_headers)


@hook('after_request')
def enable_cors():
    for key, value in cors_headers.items():
       response.set_header(key, value)


@route('/isa-json2tab/json2tab', method='POST')
def convert_isa():
    tmp_dir = mkdtemp()
    with open(tmp_dir + "/request.json", "wb") as f:
      f.write(request.body.read())
    with open(tmp_dir + '/request.json') as file_pointer:
      try:
        mkdir(tmp_dir + "/outdir")
        json2isatab.convert(file_pointer, tmp_dir + '/outdir/', validate_first=False)
      # We have to catch FileNotFound errors because the converstion tries to copy data files which
      # are not existent.
      except FileNotFoundError:
        pass
    make_archive(tmp_dir + "/isa-tab", 'zip', tmp_dir + '/outdir')
    with open(tmp_dir + '/isa-tab.zip', mode='rb') as file: # b is important -> binary
      fileContent = file.read()
    print(tmp_dir + '/isa-tab.zip')
    response.content_type = 'application/zip'
    response.set_header('Content-Description', 'File Transfer')
    response.set_header('Content-Disposition', 'attachment; filename=isa-tab.zip')
    response.set_header('Expires', '0')
    response.set_header('Cache-Control', 'must-revalidate, post-check=0, pre-check=0')
    rmtree(tmp_dir)
    return fileContent

run(host='0.0.0.0', port=8080)
