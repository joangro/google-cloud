/**
 * Copyright 2017, Google, Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

const trace = require('@google-cloud/trace-agent').start();
'use strict';

// [START gae_flex_quickstart]
const express = require('express');
const {LoggingBunyan} = require('@google-cloud/logging-bunyan');
const bunyan = require('bunyan');
const {Logging} = require('@google-cloud/logging');


const app = express();



app.get('/', (req, res) => {
  res.status(200).send('Hello, world!').end();
});

app.post('/post', (req, res) => {
  /*
  const bunyan = require('bunyan');
  const {LoggingBunyan} = require('@google-cloud/logging-bunyan');

  const trace = require('@google-cloud/trace-agent').get();
  const loggingBunyan = new LoggingBunyan({
  serviceContext: {
    service: 'java', // required to report logged errors
                           // to the Google Cloud Error Reporting
                           // console
    version: 'test'
  }
  });
  //const logging = new Logging();
  const logger = bunyan.createLogger({
	name:'java',
	streams: [
        // Log to the console
        {stream: process.stdout, level: 'info'},
        // And log to Stackdriver Logging
        loggingBunyan.stream('info'),
        ],
     
  });
  logger.error('first message')
  logger.info('nested message')

  const log = logging.log(request.PostData);
  const metadata = {
	resource: {
		"type":"gae_app",
		"labels":{
			"project_id":"wave16-joan",
			"module_id": "java",
			"version_id": "test"
		},
	},
  };
  const entry = log.entry(metadata, {delegate: "Hello post"});

  log.write(entry, (err, apiResponse) => {
  	if(!err){
		console.log('Success');
	}
  });
  log.info(entry)
  log.alert(entry)*/
  const {Logging} = require('@google-cloud/logging');
  const projectId = 'wave16-joan';
  const logging = new Logging({
    projectId: projectId,
  });
  const logName = 'request-log';
  const logger = logging.log(logName);
  const metadata = {
  resource: {
	type: 'global',
	},
  };
  const entry = logger.entry(metadata, {delegate: 'test'});
  logger.write(entry).then(logger.alert(entry));
  res.status(200).end()

});

// Start the server
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`App listening on port ${PORT}`);
  console.log('Press Ctrl+C to quit.');
});
// [END gae_flex_quickstart]
