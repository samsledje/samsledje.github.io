# Personal Website

## Setting up the dev environment

Installation is easiest with [homebrew](https://brew.sh/).

```bash
brew install ruby
brew install node
brew install --cask mactex
gem install bundler
rm Gemfile.lock
bundle install
```

## Preparing Files

```bash
make
```

## Local Serving

```bash
make serve
```

## Build CV PDF only

```bash
make cv
```

## Subdomain Records

### Software
- `conplex.samsl.io` --> https://cb.csail.mit.edu/conplex/
- `dscript.samsl.io` --> https://dscript.csail.mit.edu/
- `treefix.samsl.io` --> https://compbio.engr.uconn.edu/software/treefix-tp/
- `virdtl.samsl.io` --> https://github.com/suz11001/virDTL

### Social
- `code.samsl.io` --> https://github.com/samsledje
- `tweets.samsl.io` --> https://twitter.com/samsledzieski

### Academic

- `papers.samsl.io` --> https://samsl.io/publications.html
- `cv.samsl.io` --> https://samsl.io/files/Samuel_Sledzieski_CV.pdf
