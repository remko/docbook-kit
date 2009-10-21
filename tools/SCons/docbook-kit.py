import SCons, os.path

def generate(env, docbookkit_dir, docbook_dir) :
  tooldir = os.path.join(docbookkit_dir, "tools", "SCons")
  env.Tool("fo", toolpath = [tooldir])
  env.Tool("xslt", toolpath = [tooldir])
  env.Tool("docbook", toolpath = [tooldir])
  env.Tool("pretty-build", toolpath = [tooldir])

  env["DOCBOOK_XSL_FO"] = docbookkit_dir + "/style/fo/docbook.xsl"
  env["DOCBOOK_XSL_HTML"] = docbookkit_dir + "/style/html/docbook.xsl"
  env["DOCBOOK_XSL_WP"] = docbookkit_dir + "/style/wordpress/docbook.xsl"
  env["DOCBOOK_XML"] = docbook_dir + "/xml/catalog.xml"
  env["FOCFG"] = "fop.cfg"

  env.Command("fop.cfg", [], 
      SCons.Action.Action('echo "<fop version=\\\"1.0\\\"><renderers><renderer mime=\\\"application/pdf\\\"><fonts><directory recursive=\\\"true\\\">docbook-kit/fonts</directory></fonts></renderer></renderers></fop>" > $TARGET', cmdstr = "$GENCOMSTR"))

def exists(env) :
  return True
