
# push manually (just in case something goes wrong)

# update version
git checkout master
version=`python _update_version.py minor`
echo $version

git add geomstats/__init__.py
git commit -m "Bump version $version"
# git push origin master


# merge into stable
git checkout stable
git merge master

git tag $version
# git push origin stable
# git push origin --tags

# # wheel
# rm -rf build
# rm -rf dist
# python setup.py sdist bdist_wheel

# # upload
# # twine upload dist/*
# twine upload --repository testpypi dist/*