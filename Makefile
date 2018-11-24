
Restatic.app:
	#pyrcc5 -o src/restatic/views/collection_rc.py src/restatic/assets/icons/collection.qrc
	pyinstaller --clean --noconfirm restatic.spec
	cp -R bin/macosx64/Sparkle.framework dist/Restatic.app/Contents/Frameworks/
	cd dist; codesign --deep --sign 'Developer ID Application: Manuel Riel (CNMSCAXT48)' Restatic.app

Restatic.dmg: Restatic.app
	# sleep 2; cd dist; zip -9rq restatic-0.1.2.zip Restatic.app
	rm -rf dist/restatic-0.1.2.dmg
	sleep 2; appdmg appdmg.json dist/restatic-0.1.2.dmg

github-release: Restatic.dmg
	hub release create --prerelease --attach=dist/restatic-0.1.2.dmg v0.1.2
	git checkout gh-pages
	git commit -m 'rebuild pages' --allow-empty
	git push origin gh-pages
	git checkout master

pypi-release:
	python setup.py sdist
	twine upload dist/restatic-0.1.2.tar.gz

bump-version:
	git log $$(git describe --tags --abbrev=0)..HEAD --pretty=format:"- %s"
	bumpversion patch
#	bumpversion minor
	git push
	git push --tags

travis-debug:
	  curl -s -X POST \
       -H "Content-Type: application/json" \
       -H "Accept: application/json" \
       -H "Travis-API-Version: 3" \
       -H "Authorization: token ${TRAVIS_TOKEN}" \
       -d '{ "quiet": true }' \
       https://api.travis-ci.org/job/${TRAVIS_JOB_ID}/debug
