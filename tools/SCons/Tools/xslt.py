import SCons.Util
import xml.dom.minidom, os

################################################################################
# XSLT processor
# Currently supports only xsltproc
################################################################################

def generate(env) :
  def generate_actions(source, target, env, for_signature) :
    if not env.has_key("XSLTSTYLESHEET") :
      raise SCons.Errors.UserError, "The XSLTSTYLESHEET construction variable must be defined"

    cmd = ["$XSLT", "--nonet", "--xinclude"]
    for (param, value) in env["XSLTPARAMS"] :
      cmd += ["--stringparam", param, value]
    cmd += ["-o", "$TARGET", "$XSLTSTYLESHEET", "$SOURCE"]
    # FIXME: It's probably not clean to do an ENV assignment globally
    env["ENV"]["XML_CATALOG_FILES"] = " ".join(env.get("XMLCATALOGS", ""))
    return SCons.Action.Action([cmd], cmdstr = "$XSLTCOMSTR")

  def modify_sources(target, source, env) :
    if len(env["FOCFG"]) > 0 :
      source.append(env["FOCFG"])
    return target, source

  def scan_xml(node, env, path) :
    dependencies = set()
    nodes = [node]
    while len(nodes) > 0 :
      node = nodes.pop()
      try :
        document = xml.dom.minidom.parseString(node.get_contents())
      except xml.parsers.expat.ExpatError:
        continue
      for include in document.getElementsByTagNameNS("http://www.w3.org/2001/XInclude", "include") :
        include_file = include.getAttribute("href")
        dependencies.add(include_file)
        if include.getAttribute("parse") != "text" :
          nodes.append(env.File(include_file))
    return list(dependencies)

  env["XSLT"] = "xsltproc"
  env["XSLTPARAMS"] = []
  env["BUILDERS"]["XSLT"] = SCons.Builder.Builder(
        generator = generate_actions,
        emitter = modify_sources,
        source_scanner = SCons.Scanner.Scanner(function = scan_xml),
        src_suffix = ".xml"
      )

def exists(env) :
  # TODO: Check for existence of an XSLT processor
  return True
