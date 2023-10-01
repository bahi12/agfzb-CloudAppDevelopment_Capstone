function main(params) {
    return new Promise(function (resolve, reject) {
      const { CloudantV1 } = require("@ibm-cloud/cloudant");
      const { IamAuthenticator } = require("ibm-cloud-sdk-core");
      const authenticator = new IamAuthenticator({
        apikey: "ZYiv6q8przFhNmxJSWs5DqjrHKgCE9vEsrx_aGEOrwuo", // TODO: Replace with your own API key
      });
      const cloudant = CloudantV1.newInstance({
        authenticator: authenticator,
      });
      cloudant.setServiceUrl("https://c7414ad6-c35f-46d0-ad48-ba9c5933788f-bluemix.cloudantnosqldb.appdomain.cloud"); // TODO: Replace with your own service URL
      dealership = parseInt(params.dealerId);
      // return reviews with this dealer id
      cloudant
        .postFind({
          db: "reviews",
          selector: {
            dealership: parseInt(params.dealerId),
          },
        })
        .then((result) => {
          let code = 200;
          if (result.result.docs.length == 0) {
            code = 404;
          }
          resolve({
            statusCode: code,
            headers: { "Content-Type": "application/json" },
            body: result.result.docs,
          });
        })
        .catch((err) => {
          reject(err);
        });
    });
  }
  
  // example invocation
  let result = main({ dealerId: [15, 23] });
  result.then((reviews) => console.log(reviews));