
'use strict';


// Imports the Google Cloud client library
const monitoring = require('@google-cloud/monitoring');

// Creates a client
const client = new monitoring.MetricServiceClient();

const request = {
  name: client.projectPath('wave16-joan'),
  metricDescriptor: {
    name: "generic_node", //Metric resource type
    description: 'New test metric',
    displayName: 'TestMetric',
    type: 'custom.googleapis.com/generic_node/new_metric_2',
    metricKind: 'GAUGE',
    valueType: 'DOUBLE',
    unit: '{TEST}',
    labels:[
       {key: 'new_key', valueType: 'STRING',description: 'This is a test metric',}	
       /*{key: 'location', valueType:'STRING', description:'asdad',},
       {key: 'namespace', valueType:'STRING', description:'asdad',},
       {key: 'node_id', valueType:'STRING', description:'asdad',},
    */],
  },
};

client
  .createMetricDescriptor(request)
  .then(results => {
    const descriptor = results[0];

    console.log('Created custom Metric:\n');
    console.log(`Name: ${descriptor.displayName}`);
    console.log(`Description: ${descriptor.description}`);
    console.log(`Type: ${descriptor.type}`);
    console.log(`Kind: ${descriptor.metricKind}`);
    console.log(`Value Type: ${descriptor.valueType}`);
    console.log(`Unit: ${descriptor.unit}`);
    console.log('Labels:');
    descriptor.labels.forEach(label => {
      console.log(
        `  ${label.key} (${label.valueType}) - ${label.description}`
      );
    });
  })
  .catch(err => {
    console.error('ERROR:', err);
  });

