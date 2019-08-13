const {Storage} = require('@google-cloud/storage');
const uuid = require('uuid/v1')

async function asyncStorage() {



	const storage = new Storage();
	const bucket = storage.bucket('grauj-gcp');
	
	var ID = uuid()
	console.log(ID)

	const filename = `/test/${ID}`;
	file = bucket.file(filename);

	const content = {'ho':'asd'};
	const callback=	await file.save(content, { resumable: false });
	/*
	file.save(content, { resumable: false }, function(err){
		if (err) {
			console.log("error");
		}
	});
*/
	//await new Promise(done => setTimeout(done, 500));
	const [is_exist] = await file.exists(); // is_exist = false
	is_exist && (await file.delete());

}

asyncStorage();
