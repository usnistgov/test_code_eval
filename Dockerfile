# Make a docker container that python3, HuggingFace, and django installed
# This is necessary for testing

# Start from a python3 debian image
FROM python:3.12.6-bookworm
RUN apt-get upgrade && apt-get update -y -qq && apt-get install -y -qq python3-sphinx texlive dvipng
RUN pip install coverage==7.8.2 scipy pandas pytest==8.3.5 pandas scikit-learn matplotlib numpy ggplot  flake8 black m2r sphinx_rtd_theme joblib gitpython
RUN pip install torch torchvision torchaudio transformers django djangorestframework markdown django-filter drf-yasg
RUN pip install sphinx==7.4.7 docutils==0.20.1