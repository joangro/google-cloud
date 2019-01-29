const Datastore = require('@google-cloud/datastore');
const datastore = new Datastore();

var query = datastore.createQuery('Book');

query.run((err, entities) => {
	var keys = Object.values(entities);
	console.log(keys);
});

