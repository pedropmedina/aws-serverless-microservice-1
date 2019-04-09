module.exports.hello = event => {
  return {
    statusCode: 200,
    body: JSON.stringify({ message: 'Hello there from serverless.' }),
    input: event
  };
};
