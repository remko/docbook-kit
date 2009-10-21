import SCons.Script, sys

def generate(env) :
  if int(SCons.Script.ARGUMENTS.get("V", 0)) == 0:
    if sys.stdout.isatty() and env["PLATFORM"] != "win32":
      env["CCCOMSTR"]             = "  \033[0;32;140mCC\033[0m     $TARGET"
      env["CXXCOMSTR"]            = "  \033[0;32;140mCXX\033[0m    $TARGET"
      env["LINKCOMSTR"]           = "  \033[0;31;140mLINK\033[0m   $TARGET"
      env["ARCOMSTR"]             = "  \033[0;31;140mAR\033[0m     $TARGET"
      env["RANLIBCOMSTR"]         = "  \033[0;31;140mRANLIB\033[0m $TARGET"
      env["QT4_RCCCOMSTR"]        = "  \033[0;34;140mRCC\033[0m    $TARGET"
      env["QT4_UICCOMSTR"]        = "  \033[0;34;140mUIC\033[0m    $TARGET"
      env["QT4_MOCFROMHCOMSTR"]   = "  \033[0;34;140mMOC\033[0m    $TARGET"
      env["QT4_MOCFROMCXXCOMSTR"] = "  \033[0;34;140mMOC\033[0m    $TARGET"
      env["GENCOMSTR"]            = "  \033[0;34;140mGEN\033[0m    $TARGET"
      env["RCCOMSTR"]             = "  \033[0;34;140mRC\033[0m     $TARGET"
      env["BUNDLECOMSTR"]         = "  \033[0;34;140mBUNDLE\033[0m $TARGET"
      env["NIBCOMSTR"]            = "  \033[0;34;140mNIB\033[0m    $TARGET"
      env["NSISCOMSTR"]           = "  \033[0;34;140mNSIS\033[0m   $TARGET"
      env["XSLTCOMSTR"]           = "  \033[0;33;140mXSLT\033[0m   $TARGET"
      env["FOCOMSTR"]             = "  \033[0;33;140mFO\033[0m     $TARGET"

    else :
      env["CCCOMSTR"]             = "  CC     $TARGET"
      env["CXXCOMSTR"]            = "  CXX    $TARGET"
      env["LINKCOMSTR"]           = "  LINK   $TARGET"
      env["ARCOMSTR"]             = "  AR     $TARGET"
      env["RANLIBCOMSTR"]         = "  RANLIB $TARGET"
      env["QT4_RCCCOMSTR"]        = "  RCC    $TARGET"
      env["QT4_UICCOMSTR"]        = "  UIC    $TARGET"
      env["QT4_MOCFROMHCOMSTR"]   = "  MOC    $TARGET"
      env["QT4_MOCFROMCXXCOMSTR"] = "  MOC    $TARGET"
      env["GENCOMSTR"]            = "  GEN    $TARGET"
      env["RCCOMSTR"]             = "  RC     $TARGET"
      env["BUNDLECOMSTR"]         = "  BUNDLE $TARGET"
      env["NIBCOMSTR"]            = "  NIB    $TARGET"
      env["NSISCOMSTR"]           = "  NSIS   $TARGET"
      env["XSLTCOMSTR"]           = "  XSLT   $TARGET"
      env["FOCOMSTR"]             = "  FO     $TARGET"

def exists(env) :
  return True
