// Imports the Google Cloud client library
const monitoring = require('@google-cloud/monitoring');

// Creates a client
const client = new monitoring.MetricServiceClient();

/**
 * TODO(developer): Uncomment and edit the following lines of code.
 */
// const projectId = 'YOUR_PROJECT_ID';

const dataPoint = {
  interval: {
    endTime: {
      seconds: Date.now() / 1000,
    },
  },
  value: {
    doubleValue: 123.45,
  },
};

const timeSeriesData = {
  metric: {
    type: 'custom.googleapis.com/generic_node/new_metric_2',
    labels: {
	new_key: 'hello',
	   },
  },
  resource: {
    type: 'generic_node',
	  labels: {
      project_id: 'wave16-joan',
	location: 'europe-west1-b',
		  namespace:'testns',
		  node_id:'1231313',
	  },
  },
  points: [dataPoint],
};

const request = {
  name: client.projectPath('wave16-joan'),
 timeSeries: [timeSeriesData],
};

client
  .createTimeSeries(request)
  .then(results => {
    console.log(`Done writing time series data.`, results[0]);
  })
  .catch(err => {
    console.error('ERROR:', err);
  });

