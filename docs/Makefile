# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    = -q -t solutions
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = _build
TRAVISDIR     = ../out

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
# the i18n builder cannot share the environment and doctrees with the others
I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
GIT_SETTED = $(shell git config user.email)

.PHONY: help clean html dirhtml singlehtml pickle json htmlhelp qthelp devhelp epub latex latexpdf text man changes linkcheck doctest gettext deploy html-es clone-gh-pages set-travis-git-config push-gh-pages pull-gh-pages

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"
	@echo "  html-es       to make standalone HTML files in Spanish"
	@echo "  dirhtml    to make HTML files named index.html in directories"
	@echo "  singlehtml to make a single large HTML file"
	@echo "  pickle     to make pickle files"
	@echo "  json       to make JSON files"
	@echo "  htmlhelp   to make HTML files and a HTML help project"
	@echo "  qthelp     to make HTML files and a qthelp project"
	@echo "  devhelp    to make HTML files and a Devhelp project"
	@echo "  epub       to make an epub"
	@echo "  latex      to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
	@echo "  latexpdf   to make LaTeX files and run them through pdflatex"
	@echo "  text       to make text files"
	@echo "  man        to make manual pages"
	@echo "  texinfo    to make Texinfo files"
	@echo "  info       to make Texinfo files and run them through makeinfo"
	@echo "  gettext    to make PO message catalogs"
	@echo "  changes    to make an overview of all changed/added/deprecated items"
	@echo "  linkcheck  to check all external links for integrity"
	@echo "  doctest    to run all doctests embedded in the documentation (if enabled)"
	@echo "  server     Serve compiled docuementation throught 8000 port"
	@echo "  clone-gh-pages     Clone your gh-pages from the repository given to prepare the deploy"
	@echo "  pull-gh-pages      Update your gh-pages from the repository given to prepare the deploy"
	@echo "  set-travis-git-config   helper to set the travis user when auto deploy"
	@echo "  deploy          Compile html and deploy to gh-pages and or master on a github repository."
	@echo "                  Considere that you need to have this global variables setted."
	@echo "                  ---------------------------------------------------------------------------------------------------------"
	@echo "                  GH_REF Reference to github project (without transport protocol defined) i.e.: github.com/user/project.git"
	@echo "                  GH_BRANCH 'master' for personal pages and 'gh-pages' for project pages"
	@echo "                  GH_COMMITER_EMAIL commiter email to commit the autocompiled element."
	@echo "                  GH_COMMITER_NAME commiter email to commit the autocompiled element."
	@echo "                  GH_TOKEN definition:"
	@echo "                  rtfd: https://help.github.com/articles/creating-an-access-token-for-command-line-use/"
	@echo "                  Considere that you can secure it for travis porpose your token rtfd: "
	@echo "                  https://docs.travis-ci.com/user/encryption-keys/"
	@echo "  push-gh-pages   Helper to push to gh-pages with global variables on .travis.yml"

pull-gh-pages:
	(cd $(BUILDDIR)/travis; git pull origin $(GH_BRANCH))
	@echo "Succesfully Updated $(GH_BRANCH)"

clone-gh-pages:
	git clone https://$(GH_REF) --branch=$(GH_BRANCH) $(BUILDDIR)/travis;
	@echo "Succesfully Clonned from gh-pages"

set-travis-git-config:
	(cd $(BUILDDIR)/travis; git config user.email $(GH_COMMITER_EMAIL); git config user.name $(GH_COMMITER_NAME))
	@echo "Git parameters Setted."

push-gh-pages:
	(cd $(BUILDDIR)/travis; git add .; git commit -m "Automatically built in travis, Build number: $(TRAVIS_BUILD_NUMBER) ")
	(cd $(BUILDDIR)/travis; git push --force --quiet "https://$(GH_TOKEN)@$(GH_REF)" $(GH_BRANCH):$(GH_BRANCH) > /dev/null 2>&1)
	@echo "Succesfully pushed"

deploy:
	test -d $(BUILDDIR)/travis && $(MAKE) pull-gh-pages || $(MAKE) clone-gh-pages
	$(MAKE) html-es
	touch $(BUILDDIR)/travis/.nojekyll;
	rsync -rv --exclude=.git $(BUILDDIR)/html/* $(BUILDDIR)/travis/
	$(if $(findstring @,$(GIT_SETTED)), @echo 'Using global parameters already Setted', $(MAKE) set-travis-git-config)
	$(MAKE) push-gh-pages
	@echo 'Commited and deployed'

html-es:
	sphinx-intl build
	$(MAKE) -e SPHINXOPTS="-D language='es'" html

clean:
	-rm -rf $(BUILDDIR)/*

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

dirhtml:
	$(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/dirhtml
	sed -i '/-99999/d' _build/dirhtml/_static/flasky.css
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/dirhtml."

singlehtml:
	$(SPHINXBUILD) -b singlehtml $(ALLSPHINXOPTS) $(BUILDDIR)/singlehtml
	@echo
	@echo "Build finished. The HTML page is in $(BUILDDIR)/singlehtml."

pickle:
	$(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) $(BUILDDIR)/pickle
	@echo
	@echo "Build finished; now you can process the pickle files."

json:
	$(SPHINXBUILD) -b json $(ALLSPHINXOPTS) $(BUILDDIR)/json
	@echo
	@echo "Build finished; now you can process the JSON files."

htmlhelp:
	$(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) $(BUILDDIR)/htmlhelp
	@echo
	@echo "Build finished; now you can run HTML Help Workshop with the" \
	      ".hhp project file in $(BUILDDIR)/htmlhelp."

qthelp:
	$(SPHINXBUILD) -b qthelp $(ALLSPHINXOPTS) $(BUILDDIR)/qthelp
	@echo
	@echo "Build finished; now you can run "qcollectiongenerator" with the" \
	      ".qhcp project file in $(BUILDDIR)/qthelp, like this:"
	@echo "# qcollectiongenerator $(BUILDDIR)/qthelp/OpenERPTechnicalDocumentation.qhcp"
	@echo "To view the help file:"
	@echo "# assistant -collectionFile $(BUILDDIR)/qthelp/OpenERPTechnicalDocumentation.qhc"

devhelp:
	$(SPHINXBUILD) -b devhelp $(ALLSPHINXOPTS) $(BUILDDIR)/devhelp
	@echo
	@echo "Build finished."
	@echo "To view the help file:"
	@echo "# mkdir -p $$HOME/.local/share/devhelp/OpenERPTechnicalDocumentation"
	@echo "# ln -s $(BUILDDIR)/devhelp $$HOME/.local/share/devhelp/OpenERPTechnicalDocumentation"
	@echo "# devhelp"

epub:
	$(SPHINXBUILD) -b epub $(ALLSPHINXOPTS) $(BUILDDIR)/epub
	@echo
	@echo "Build finished. The epub file is in $(BUILDDIR)/epub."

latex:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo
	@echo "Build finished; the LaTeX files are in $(BUILDDIR)/latex."
	@echo "Run \`make' in that directory to run these through (pdf)latex" \
	      "(use \`make latexpdf' here to do that automatically)."

latexpdf:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo "Running LaTeX files through pdflatex..."
	$(MAKE) -C $(BUILDDIR)/latex all-pdf
	@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex."

text:
	$(SPHINXBUILD) -b text $(ALLSPHINXOPTS) $(BUILDDIR)/text
	@echo
	@echo "Build finished. The text files are in $(BUILDDIR)/text."

man:
	$(SPHINXBUILD) -b man $(ALLSPHINXOPTS) $(BUILDDIR)/man
	@echo
	@echo "Build finished. The manual pages are in $(BUILDDIR)/man."

texinfo:
	$(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(BUILDDIR)/texinfo
	@echo
	@echo "Build finished. The Texinfo files are in $(BUILDDIR)/texinfo."
	@echo "Run \`make' in that directory to run these through makeinfo" \
	      "(use \`make info' here to do that automatically)."

info:
	$(SPHINXBUILD) -b texinfo $(ALLSPHINXOPTS) $(BUILDDIR)/texinfo
	@echo "Running Texinfo files through makeinfo..."
	make -C $(BUILDDIR)/texinfo info
	@echo "makeinfo finished; the Info files are in $(BUILDDIR)/texinfo."

gettext:
	$(SPHINXBUILD) -b gettext $(I18NSPHINXOPTS) $(BUILDDIR)/locale
	@echo
	@echo "Build finished. The message catalogs are in $(BUILDDIR)/locale."

changes:
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) $(BUILDDIR)/changes
	@echo
	@echo "The overview file is in $(BUILDDIR)/changes."

linkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

doctest:
	$(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) $(BUILDDIR)/doctest
	@echo "Testing of doctests in the sources finished, look at the " \
	      "results in $(BUILDDIR)/doctest/output.txt."

pseudoxml:
	$(SPHINXBUILD) -b pseudoxml $(ALLSPHINXOPTS) $(BUILDDIR)/pseudoxml
	@echo
	@echo "Build finished. The pseudo-XML files are in $(BUILDDIR)/pseudoxml."

serve:
	(cd $(BUILDDIR)/html; python -m SimpleHTTPServer 8000)
