# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# TODO: Address all TODOs and remove all explanatory comments
"""TODO: Add a description here."""


import csv
import json
import os

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
https://github.com/bebetterest/JJQA
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
JJQA: a Chinese QA dataset on the lyrics of JJ Lin's songs.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://github.com/bebetterest/JJQA"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "Apache-2.0 license"

# TODO: Add link to the official dataset URLs here
# The HuggingFace Datasets library doesn't host the datasets but only points to the original files.
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLS = {
    "qa": "hf_q_a.json",
    "song": "hf_song.json",
    "song_index": "hf_song_indx.json"
}


# TODO: Name of the dataset usually matches the script name with CamelCase instead of snake_case
class JJQA(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("0.0.1")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="qa", version=VERSION, description="This part of my dataset covers a first domain"),
        datasets.BuilderConfig(name="song", version=VERSION, description="This part of my dataset covers a second domain"),
        datasets.BuilderConfig(name="song_index", version=VERSION, description="This part of my dataset covers a first domain"),
    ]

    DEFAULT_CONFIG_NAME = "qa"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        if self.config.name == "qa":  # This is the name of the configuration selected in BUILDER_CONFIGS above
            description=_DESCRIPTION+" This is the field with Q&As."
            features = datasets.Features(
                {
                    "q": datasets.Value("string"),
                    "a": datasets.Value("string"),
                    "rf": datasets.Value("string"),
                    "song_title": datasets.Value("string"),
                    "song_id": datasets.Value("string"),
                    "id": datasets.Value("string"),
                    # These are the features of your dataset like images, labels ...
                }
            )
        elif self.config.name == "song":
            description=_DESCRIPTION+" This is the field with songs."
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "name": datasets.Value("string"),
                    "lyric": datasets.Value("string"),
                    # These are the features of your dataset like images, labels ...
                }
            )
        else:  # This is an example to show how to have different features for "first_domain" and "second_domain"
            description=_DESCRIPTION+" This is the field with a song_id-index dict."
            features = datasets.Features(
                {   
                    "dic": datasets.Value("string"),
                    # These are the features of your dataset like images, labels ...
                }
            )

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=description,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features, uncomment supervised_keys line below and
            # specify them. They'll be used if as_supervised=True in builder.as_dataset.
            # supervised_keys=("sentence", "label"),
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLS
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        urls = _URLS[self.config.name]
        data_dir = dl_manager.download_and_extract(urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir,
                    # "split": "train",
                },
            )
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, filepath):
        # TODO: This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is for legacy reasons (tfds) and is not important in itself, but must be unique for each example.
        tmp=None
        with open(filepath, encoding="utf-8") as f:
            tmp=json.load(f)["data"]
        if(self.config.name=="qa"):
            for key, row in enumerate(tmp):
                yield key, {
                    "q": row["q"],
                    "a": row["a"],
                    "rf": row["rf"],
                    "song_title": row["song_title"],
                    "song_id": row["song_id"],
                    "id": row["id"],
                }
        elif(self.config.name=="song"):
            for key, row in enumerate(tmp):
                yield key, {
                    "id": row["id"],
                    "title": row["title"],
                    "name": row["name"],
                    "lyric": row["lyric"],
                }
        else:
            yield 0,{
                "dic":json.dumps(tmp)
            }
