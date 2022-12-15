from bottle import route, run, template, response, request
from isatools.convert import json2isatab
from tempfile import mkdtemp
from shutil import rmtree, make_archive
from os import mkdir

@route('/json2tab', method='OPTIONS')
def allow_cors():
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header("Access-Control-Allow-Methods", "OPTIONS,POST")
    response.set_header("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, Origin, Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers");

@route('/json2tab', method='POST')
def do_login():
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Headers', '*/*')
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
