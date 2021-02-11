#!/usr/bin/env bash

gcloud functions deploy delivery --runtime python38 --trigger-http --allow-unauthenticated \
	 --set-env-vars EMAIL=$_EMAIL \
	 --set-env-vars PASSWORD=$_PASSOWRD \
	 --set-env-vars HEADLESS=$_HEADLESS  \
	 --project $_PROJECT \
	 --region $_REGION 
