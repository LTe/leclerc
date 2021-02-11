#!/usr/bin/env bash

gcloud functions deploy delivery --runtime python38 --trigger-http --allow-unauthenticated \
	 --set-env-vars EMAIL=$EMAIL \
	 --set-env-vars PASSWORD=$PASSWORD \
	 --set-env-vars HEADLESS=$HEADLESS \
	 --project $PROJECT \
	 --region $REGION 
