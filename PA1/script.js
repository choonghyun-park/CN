function sleepMs(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function scriptVersion(){
	return "v1.0.0 (20230330 ed1)"
}

// Fetch: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
async function fetchResult(url = "", method = "GET", data = {}, jsonHeader = false) {
    const fetchInit = {
        method: method, // *GET, POST, PUT, DELETE
        mode: "cors", // no-cors, *cors, same-origin
        cache: "default", // *default, no-cache
        credentials: "same-origin",
        headers: {
            // json 명시 시 OPTIONS preflight 발송되므로 생략
            // no-cors인 경우 application/json 불가능
        }
    };
    if (method == "PUT" || method == "POST") {
        fetchInit['body'] = JSON.stringify(data);
    }
    if(jsonHeader){
        fetchInit.headers["Content-Type"] = "application/json";
    }
    console.log("[REQ] Request sent to " + url + " with method " + method + (
        fetchInit['body']?(" and data " + fetchInit['body'] +
            (jsonHeader?" with Content-Type header value of application/json":"")):""));
    await sleepMs(200);
    const response = await fetch(url, fetchInit);
    console.log("[REQ] Got response, status " + response.status);
    return response;
}



// Send get request to /hi and check it is 200 OK and response is {"message": "hi"}
async function test1() {
    let successCount = 0;
    await fetchResult("http://localhost:1398/hi", "GET").then(async (response) => {
        //check status code is 200 OK
        if (response.status === 200) {
            //check response is {"message": "hi"}
            await response.json().then((json) => {
                if(json.message !== "hi"){
                    console.log("test1 fail. Expected: hi, Got: " + json.message);
                    return;
                }
                successCount++;
                console.log("test1 success")
            });
        } else {
            console.log("test1 fail. Expected 200, but got: " + response.status);
        }
    })
    return successCount === 1;
}

// Send POST request to /echo with {"message": "..."} and check it is 200 OK and response is {"message": "..."}
// Message is generated randomly and length is 2 to 10
// Test for 20 times
async function test2() {
    let successCount = 0;
    for (let i = 0; i < 20; i++) {
        const length = Math.floor(Math.random() * (10 - 2 + 1)) + 2;
        // generate alphanumeric string with given length
        let message = "";
        for (let i = 0; i < length; i++) {
            const targetCharacters = "abcdefghijklmnopqrstuvwxyz0123456789";
            message += targetCharacters.charAt(Math.floor(Math.random() * targetCharacters.length));
        }
        await fetchResult("http://localhost:1398/echo", "POST", {"message": message}).then(async (response) => {
            //check status code is 200 OK
            if (response.status === 200) {
                // cast response to json
                await response.json().then((json) => {
                    //check response is {"message": "..."}
                    if (json.message === message) {
                        console.log("Successfully echoed message " + message)
                        successCount++;
                    } else {
                        console.log("test2 fail. Expected: " + json.message + ", Got: " + message);
                    }
                });
            }
            else{
                console.log("Expected 200, but got: " + response.status);
            }
        });
    }
    console.log("test2 success count: " + successCount);
    return successCount === 20;
}

// Send GET request to /... and check it is 404
// ... is generated randomly and length is 2 to 10 but not "hi", "echo", or "user"
// test 20 times
async function test3() {
    let successCount = 0;
    for (let i = 0; i < 20; i++) {
        let message = "";
        const length = Math.floor(Math.random() * (10 - 2 + 1)) + 2;
        // generate lowercase string with given length
        for (let i = 0; i < length; i++) {
            const targetCharacters = "abcdefghijklmnopqrstuvwxyz";
            message += targetCharacters.charAt(Math.floor(Math.random() * targetCharacters.length));
        }
        if (message === "hi" || message === "echo" || message === "user") {
            i--;
            continue;
        }
        await fetchResult("http://localhost:1398/" + message, "GET").then((response) => {
            //check status code is 404
            if (response.status === 404) {
                console.log("Successfully got 404")
                successCount++;
            }
            else{
                console.log("Expected 404, but got: " + response.status);
            }
        });

    }

    console.log("test3 success count: " + successCount);
    return successCount === 20;
}

// Send GET request to /user?id=... and check it is 404 Not Found
// ... is generated randomly and length is 2 to 6
// Test for 20 times
async function test4() {
    let successCount = 0;
    for (let i = 0; i < 20; i++) {
        let id = generateRandomId(2, 6);
        await fetchResult("http://localhost:1398/user?id=" + id, "GET").then((response) => {
            //check status code is 404 Not Found
            if (response.status === 404) {
                console.log("Successfully got 404")
                successCount++;
            }
            else{
                console.log("Expected 404, but got: " + response.status);
            }
        })
    }
    console.log("test4 success count: " + successCount);
    return successCount === 20;
}

// generate random ID with given length range. It is alphanumeric
function generateRandomId(lengthMin, lengthMax) {
    const length = Math.floor(Math.random() * (lengthMax - lengthMin + 1)) + lengthMin;
    // generate alphanumeric string with given length
    let result = "";
    for (let i = 0; i < length; i++) {
        const targetCharacters = "abcdefghijklmnopqrstuvwxyz0123456789";
        result += targetCharacters.charAt(Math.floor(Math.random() * targetCharacters.length));
    }
    return result;
}

// generate random name with given length range. It is lowercase alphabets
function generateRandomName(lengthMin, lengthMax) {
    const length = Math.floor(Math.random() * (lengthMax - lengthMin + 1)) + lengthMin;
    // generate lowercase alphabets string with given length
    let result = "";
    for (let i = 0; i < length; i++) {
        const targetCharacters = "abcdefghijklmnopqrstuvwxyz";
        result += targetCharacters.charAt(Math.floor(Math.random() * targetCharacters.length));
    }
    return result;
}

// generate random gender. It is "male" or "female".
function generateRandomGender() {
    if (Math.random() < 1.0 / 2.0) {
        return "male";
    } else {
        return "female";
    }
}

// Send POST request to /user with user information and check it is 201 Created or 409 Conflict or 400 Bad Request
// User information is consist of name, gender, and id
// Generate name randomly, it is english alphabet and length is 2 to 10
// Generate gender randomly, it is "male" or "female"
// Generate id randomly, it is alphanumeric. For this test, length is 3 to 4
// 400 Bad Request is checked by sending empty data or missing name, gender, or id
// 201 Created is checked by sending normal new user information
// 409 Conflict is checked by sending normal user information whose id is already registered
// Test 40 times, including more than 8 times of each(400, 201, 409), order is random
async function test5() {
    // setting up order
    const order = [];
    // set up 8 invalid, and 10 valid
    for (let i = 0; i < 8; i++) {
        order.push("invalid");
    }
    for (let i = 0; i < 16; i++) {
        order.push("valid");
    }
    // randomly add rest 16 items with weight of 1 on invalid, 2 on valid
    for (let i = 0; i < 16; i++) {
        if (Math.random() < 1.0 / 3.0) {
            order.push("invalid");
        } else {
            order.push("valid");
        }
    }
    // shuffle order
    for (let i = order.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [order[i], order[j]] = [order[j], order[i]];
    }

    // count how many "valid" in order
    let validCount = 0;
    for (let i = 0; i < order.length; i++) {
        if (order[i] === "valid") {
            validCount++;
        }
    }
    // divide valid into 201 and 409
    // add guaranteed 8 items first (201 is 7 items because it will be added in front of valid later)
    const valids = [];
    for (let i = 0; i < 7; i++) {
        valids.push("201");
    }
    for (let i = 0; i < 8; i++) {
        valids.push("409");
    }
    // randomly add 201 and 409 for rest of valid
    for (let i = 0; i < validCount - 16; i++) {
        if (Math.random() < 0.5) {
            valids.push("201");
        } else {
            valids.push("409");
        }
    }
    // shuffle valids
    for (let i = valids.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [valids[i], valids[j]] = [valids[j], valids[i]];
    }
    // insert 201 at the front of valid - actually at the back is the first
    valids.push("201");

    // divide invalid to what is missing
    // make map with which data to be missed, one, two, or three among id, gender, and name
    // each missing cases must be guaranteed and generated randomly for rest of invalid
    let invalidCount = 40 - validCount;
    const invalids = [];
    invalids.push(["id"])
    invalids.push(["gender"])
    invalids.push(["name"])
    invalids.push(["id", "gender"])
    invalids.push(["id", "name"])
    invalids.push(["gender", "name"])
    invalids.push(["id", "gender", "name"])
    for (let i = 0; i < invalidCount - 7; i++) {
        // randomly choose one, two, or three then push
        const missing = [];
        if (Math.random() < 1.0 / 3.0) {
            missing.push("id");
        }
        if (Math.random() < 1.0 / 3.0) {
            missing.push("gender")
        }
        if (Math.random() < 1.0 / 3.0) {
            missing.push("name")
        }
        // missing must not be empty
        if (missing.length === 0) {
            i--;
            continue;
        }
        invalids.push(missing);
    }
    // shuffle invalids
    for (let i = invalids.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [invalids[i], invalids[j]] = [invalids[j], invalids[i]];
    }


    // start test
    let successCount = 0;
    let failCount = 0;
    let requestedIds = [];
    for (let i = 0; i < order.length; i++) {
        // invalid
        if (order[i] === "invalid") {
            // test for invalid data
            const missing = invalids.pop();
            const data = {};
            if (!missing.includes("id")) {
                data.id = generateRandomId(3, 4);
            }
            if (!missing.includes("name")) {
                data.name = generateRandomName(2, 10);
            }
            if (!missing.includes("gender")) {
                data.gender = generateRandomGender();
            }
            // send post
            await fetchResult("http://localhost:1398/user", "POST", data).then(result => {
                if (result.status === 400) {
                    console.log("Successfully got 400 with missing " + missing);
                    successCount++;
                } else {
                    failCount++;
                    console.log("Expected 400 but got " + result.status)
                }
            });
        } else {
            // valid
            // test for valid data
            const valid = valids.pop();
            const data = {};
            if (valid === "201") {
                // generate data
                data.id = generateRandomId(3, 4);
                while (requestedIds.includes(data.id)) {
                    data.id = generateRandomId(3, 4);
                }
                data.name = generateRandomName(2, 10);
                data.gender = generateRandomGender();
                // send post
                await fetchResult("http://localhost:1398/user", "POST", data).then(result => {
                    if (result.status === 201) {
                        successCount++;
                        console.log("Successfully got 201 with id " + data.id);
                        requestedIds.push(data.id);
                    } else {
                        failCount++;
                        console.log("Expected 201 but got " + result.status);
                    }
                });
            } else {
                // generate data but take id from already requested ids
                data.id = requestedIds[Math.floor(Math.random() * requestedIds.length) | 0];
                data.name = generateRandomName(2, 10);
                data.gender = generateRandomGender();
                // send post
                await fetchResult("http://localhost:1398/user", "POST", data).then(result => {
                    if (result.status === 409) {
                        console.log("Successfully got 409 with id " + data.id);
                        successCount++;
                    } else {
                        failCount++;
                        console.log("Expected 409 but got " + result.status)
                    }
                });
            }
        }
    }

    console.log("test5 success: " + successCount + ", fail: " + failCount);
    return successCount === 40;
}

// Send 20 valid POST requests
// Then test for GET /user?id=<id> for each id
// This time, id is len 5~6 for separated test
async function test6() {
    const sentData = [];
    const generatedIds = [];
    for (let i = 0; i < 20; i++) {
        // send post and save data
        const data = {};
        data.id = generateRandomId(5, 6);
        while (generatedIds.includes(data.id)) {
            data.id = generateRandomId(5, 6);
        }
        generatedIds.push(data.id);
        data.name = generateRandomName(2, 10);
        data.gender = generateRandomGender();
        await fetchResult("http://localhost:1398/user", "POST", data).then(result => {
            if (result.status === 201) {
                console.log("Successfully registered user " + data.id);
                sentData.push(data);
            } else {
                console.log("Expected 201 but got " + result.status);
            }
        });
    }
    if (sentData.length !== 20) {
        console.log("test6 failed while sending POST requests");
        return;
    }

    // shuffle sentData order
    for (let i = sentData.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [sentData[i], sentData[j]] = [sentData[j], sentData[i]];
    }

    // test for GET /user?id=<id>
    let successCount = 0;
    let failCount = 0;
    for (let i = 0; i < sentData.length; i++) {
        await fetchResult("http://localhost:1398/user?id=" + sentData[i].id, "GET").then(async result => {
            if (result.status === 200) {
                // check body json is equal to data
                await result.json().then(json => {
                    // check json data and sent data are equal
                    if (sentData[i].id === json.id && sentData[i].name === json.name && sentData[i].gender === json.gender) {
                        successCount++;
                        console.log("Successfully got 200 and proper data with id " + sentData[i].id);
                    } else {
                        failCount++;
                        console.log("Got 200 but data is wrong, expected " + sentData[i] + " but got " + json);
                    }
                });
            } else {
                failCount++;
                console.log("Expected 200 but got " + result.status);
            }
        });
    }

    console.log("test6 success: " + successCount + ", fail: " + failCount);
    return successCount === 20;
}

// Here, test for preflight request
// Just send 1 Post request with id 1
// Then request with OPTIONS method to /user/1 and figure out it returns
// Cannot check Access-Control-Allow-* because it is forbidden
// It will be checked in further tests
async function test7() {
    let successCount = 0;
    const data = {};
    data.id = "1";
    data.name = generateRandomName(2, 10);
    data.gender = generateRandomGender();
    await fetchResult("http://localhost:1398/user", "POST", data).then(async result => {
        if (result.status === 201) {
            console.log("Successfully registered user " + data.id);
            // send preflight request
            await fetchResult("http://localhost:1398/user/1", "OPTIONS").then(result => {
                if (result.status === 200) {
                    console.log("Successfully got 200 with OPTIONS");
                    successCount++;
                } else {
                    console.log("Expected 200 but got " + result.status);
                }
            });
        } else {
            console.log("test7 failed while sending POST request");
        }
    });
    await fetchResult("http://localhost:1398/user", "OPTIONS").then(result => {
        if (result.status === 200) {
            console.log("Successfully got 200 with OPTIONS");
            successCount++;
        } else {
            console.log("Expected 200 but got " + result.status);
        }
    });
    console.log("test7 success: " + successCount + ", fail: " + (2 - successCount));

    return successCount === 2;
}

// This time, id is length 7~8 for separated test
// Send 20 valid POST requests
// Send 15 DELETE requests(5 404 request and 10 valid request), meantime send verifying GET requests
async function test8() {
    const sentData = [];
    const generatedIds = [];
    for (let i = 0; i < 20; i++) {
        const data = {};
        data.id = generateRandomId(7, 8);
        while (generatedIds.includes(data.id)) {
            data.id = generateRandomId(7, 8);
        }
        generatedIds.push(data.id);
        data.name = generateRandomName(2, 10);
        data.gender = generateRandomGender();
        await fetchResult("http://localhost:1398/user", "POST", data, true).then(result => {
            if (result.status === 201) {
                console.log("Successfully registered user " + data.id);
                sentData.push(data);
            } else {
                console.log("Expected 201 but got " + result.status);
            }
        });
    }
    if (sentData.length !== 20) {
        console.log("test7 failed while sending POST requests");
        return;
    }

    // shuffle sentData order
    for (let i = sentData.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [sentData[i], sentData[j]] = [sentData[j], sentData[i]];
    }
    const deletedData = [];

    // send delete and get requests.
    const requests = [];
    for (let i = 0; i < 5; i++) {
        requests.push("not-existing");
    }
    for (let i = 0; i < 10; i++) {
        requests.push("existing");
    }
    for (let i = requests.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [requests[i], requests[j]] = [requests[j], requests[i]];
    }

    let successCount = 0;
    let failCount = 0;
    for (let i = 0; i < 15; i++) {
        if (requests[i] === "not-existing") { // test for id that is not existing and getting 404
            let idToBeDeleted = generateRandomId(7, 8);
            while (sentData.includes(idToBeDeleted)) {
                idToBeDeleted = generateRandomId(7, 8);
            }
            await fetchResult("http://localhost:1398/user/" + idToBeDeleted, "DELETE").then(async result => {
                if (result.status === 404) {
                    console.log("Successfully got 404 with deleting id " + idToBeDeleted);
                    successCount++;
                } else {
                    failCount++;
                    console.log("Expected 404 but got " + result.status);
                }
            });
        } else {
            let idToBeDeleted = sentData.pop().id;
            await fetchResult("http://localhost:1398/user/" + idToBeDeleted, "DELETE").then(async result => {
                if (result.status === 200) {
                    console.log("Successfully deleted user " + idToBeDeleted);
                    deletedData.push(idToBeDeleted);
                } else {
                    failCount++;
                    console.log("Expected 200 but got " + result.status);
                }
            });
            let verifyDeletedId = deletedData[Math.floor(Math.random() * deletedData.length)];
            let verifySentId = sentData[Math.floor(Math.random() * sentData.length)].id;
            let idList = [verifyDeletedId, verifySentId];
            if (Math.random() < 0.5) { // random shuffle
                [idList[0], idList[1]] = [idList[1], idList[0]];
            }
            for (let id of idList) {
                await fetchResult("http://localhost:1398/user?id=" + id, "GET").then(async result => {
                    if (id === verifyDeletedId) {
                        if (result.status === 404) {
                            successCount++;
                            console.log("Successfully got 404 with id " + id);
                        } else {
                            failCount++;
                            console.log("Expected 404 but got " + result.status);
                        }
                    } else { // id === verifySentId
                        if (result.status === 200) {
                            successCount++;
                            console.log("Successfully got 200 with id " + id);
                        } else {
                            failCount++;
                            console.log("Expected 200 but got " + result.status);
                        }
                    }
                });
            }
        }
    }

    console.log("test8 success: " + successCount + ", fail: " + failCount);
    return successCount === 25;
}

// This time, id is length 9~12 for separated test
// Send 20 valid POST requests
// Send 40 PUT requests including invalid requests, meantime send verifying GET requests
async function test9() {
    const sentData = [];
    const generatedIds = [];
    for (let i = 0; i < 20; i++) {
        let data = {};
        data.id = generateRandomId(9, 12);
        while (generatedIds.includes(data.id)) {
            data.id = generateRandomId(9, 12);
        }
        generatedIds.push(data.id);
        data.name = generateRandomName(2, 10);
        data.gender = generateRandomGender();
        await fetchResult("http://localhost:1398/user", "POST", data, true).then(result => {
            if (result.status === 201) {
                console.log("Successfully registered user " + data.id);
                sentData.push(data);
            } else {
                console.log("Expected 201 but got " + result.status);
            }
        });
    }
    if (sentData.length !== 20) {
        console.log("test9 failed while sending POST requests");
        return;
    }

    // shuffle sentData order
    for (let i = sentData.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [sentData[i], sentData[j]] = [sentData[j], sentData[i]];
    }

    // put request must contains 10+ 400 response, 5+ 200 response, 3+ 422 response, 3+ 404 response

    const types = [];
    let count400 = 10, count200 = 5, count422 = 3, count404 = 3;
    for (let i = 0; i < 10; i++) types.push("400");
    for (let i = 0; i < 5; i++) types.push("200");
    for (let i = 0; i < 3; i++) types.push("422");
    for (let i = 0; i < 3; i++) types.push("404");
    while (types.length < 40) {
        switch (Math.floor(Math.random() * 4)) {
            case 0:
                types.push("400");
                count400++;
                break;
            case 1:
                types.push("200");
                count200++;
                break;
            case 2:
                types.push("422");
                count422++;
                break;
            case 3:
                types.push("404");
                count404++;
                break;
        }
    }
    for (let i = types.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [types[i], types[j]] = [types[j], types[i]];
    }

    // prepare 400 first
    const invalidMissings = [];
    invalidMissings.push(["id"])
    invalidMissings.push(["name"])
    invalidMissings.push(["gender"])
    // id, gender missing is right data
    invalidMissings.push(["id", "name"])
    invalidMissings.push(["gender", "name"])
    invalidMissings.push(["id", "gender", "name"])
    invalidMissings.push([])
    while (invalidMissings.length < count400) {
        let random = Math.floor(Math.random() * 7);
        invalidMissings.push(invalidMissings[random]);
    }
    for (let i = invalidMissings.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [invalidMissings[i], invalidMissings[j]] = [invalidMissings[j], invalidMissings[i]];
    }

    // start sending
    let successCount = 0, failCount = 0;
    for (let i = 0; i < 40; i++) {
        switch (types[i]) {
            case "400":
                let invalidMissing = invalidMissings.pop();
                let invalidData = {};
                let takingTarget = sentData[Math.floor(Math.random() * sentData.length)];
                if (!invalidMissing.includes("id")) {
                    invalidData.id = takingTarget.id;
                }
                if (!invalidMissing.includes("name")) {
                    invalidData.name = takingTarget.name;

                }
                if (!invalidMissing.includes("gender")) {
                    invalidData.gender = takingTarget.gender;
                }
                await fetchResult("http://localhost:1398/user/" + takingTarget.id, "PUT", invalidData, true).then(result => {                    if (result.status === 400) {
                        successCount++;
                        console.log("Successfully got 400 with missing " + invalidMissing);
                    } else {
                        failCount++;
                        console.log("Expected 400 but got " + result.status + " with missing " + invalidMissing);
                    }
                });
                break;
            case "200":
                const validTarget = Math.floor(Math.random() * sentData.length);
                let changingName = generateRandomName(2, 10);
                while (changingName === sentData[validTarget].name) {
                    changingName = generateRandomName(2, 10);
                }
                await fetchResult("http://localhost:1398/user/" + sentData[validTarget].id, "PUT", {name: changingName}, true).then(async result => {
                    if (result.status === 200) {
                        sentData[validTarget].name = changingName;
                        console.log("Successfully got 200 with changing name, checking with GET...");
                        await fetchResult("http://localhost:1398/user?id=" + sentData[validTarget].id, "GET").then(async result => {
                            if (result.status === 200) {
                                await result.json().then(result => {
                                    if (result.name === sentData[validTarget].name && result.id === sentData[validTarget].id && result.gender === sentData[validTarget].gender) {
                                        successCount++;
                                        console.log("Successfully proper data with changing name");
                                    } else {
                                        failCount++;
                                        console.log("Got 200 for GET but wrong data: " + JSON.stringify(result.data) + ", expected: " + JSON.stringify(sentData[validTarget]));
                                    }
                                });
                            } else {
                                failCount++;
                                console.log("Expected 200 but got " + result.status + " on GET request");
                            }
                        });
                    } else {
                        failCount++;
                        console.log("Expected 200 but got " + result.status + " with changing name");
                    }
                });
                break;
            case "422": // send same name and check 422
                const target422 = Math.floor(Math.random() * sentData.length);
                await fetchResult("http://localhost:1398/user/" + sentData[target422].id, "PUT", {name: sentData[target422].name}, true).then(result => {
                    if (result.status === 422) {
                        successCount++;
                        console.log("Successfully got 422 with same name");
                    } else {
                        failCount++;
                        console.log("Expected 422 but got " + result.status + " with same name");
                    }
                });
                break;
            case "404":
                let invalidId = generateRandomId(9, 12);
                while (sentData.some(data => data.id === invalidId)) {
                    invalidId = generateRandomId(9, 12);
                }
                await fetchResult("http://localhost:1398/user/" + invalidId, "PUT", {name: generateRandomName(2, 10)}, true).then(result => {
                    if (result.status === 404) {
                        successCount++;
                        console.log("Successfully got 404 with invalid id");
                    } else {
                        failCount++;
                        console.log("Expected 404 but got " + result.status + " with invalid id");
                    }
                });
                break;
        }


    }
    console.log("test9 Success: " + successCount + ", Fail: " + failCount);
    return successCount === 40;
}
