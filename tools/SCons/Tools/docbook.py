import SCons.Util
import xml.dom.minidom, re, os.path

################################################################################
# DocBook pseudobuilder
################################################################################

def generate(env) :
  def remove_doctype(target, source, env) :
    f = open(str(target[0]))
    output = []
    for line in f.readlines() :
      output.append(re.sub("^<!DOCTYPE .*", "", line))
    f.close()
    f = open(str(target[0]), 'wb')
    for line in output :
      f.write(line)
    f.close()

  def buildDocBook(env, source) :
    db_env = env.Clone()
    db_env["XMLCATALOGS"] = [db_env["DOCBOOK_XML"]]

    # PDF generation
    fo = db_env.XSLT(os.path.splitext(source)[0] + ".fo", source, 
        XSLTSTYLESHEET = db_env["DOCBOOK_XSL_FO"])
    pdf = db_env.FO(fo)

    # HTML generation
    db_env.XSLT(os.path.splitext(source)[0] + ".html", source, 
        XSLTSTYLESHEET = db_env["DOCBOOK_XSL_HTML"])

    # WordPress generation
    wp_params = [("wordpress.dir", env.get("DOCBOOK_WP_DIR", "../../wordpress"))]
    wp_pdf_url = env.get("DOCBOOK_WP_PDF_URL", pdf[0].name)
    if len(wp_pdf_url) > 0 :
      wp_params.append(("pdf.url", wp_pdf_url))
      wp_params.append(("pdf.icon", env.get("DOCBOOK_WP_PDF_ICON", "/icons/pdf.png")))
    wp = db_env.XSLT(os.path.splitext(source)[0] + ".wp.php", source, 
        XSLTSTYLESHEET = db_env["DOCBOOK_XSL_WP"],
        XSLTPARAMS = wp_params + env.get("XSLTPARAMS", []))
    db_env.AddPostAction(wp, remove_doctype)

  env.AddMethod(buildDocBook, "DocBook")
      
def exists(env) :
  return True
