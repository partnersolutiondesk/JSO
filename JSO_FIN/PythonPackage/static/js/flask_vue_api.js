
function getCustomerDetails(){
url=window.location.href
const [hash, query] = url.split('#')[1].split('?')
const params = Object.fromEntries(new URLSearchParams(query))

console.log(hash)
console.log(params)

//console.log(window.location)
//const urlParams = new URLSearchParams(window.location.href.search);
      var customerID = params.id;
      console.log("custID"+customerID)
        //customerID="65096869bfc509458f6e1622"
         return axios.post('http://localhost:5000/jso/getCustomerDetails',{id: customerID}).then((response) => {
            console.log(response.data.CustomerDetails)
            val=JSON.parse(response.data.CustomerDetails)
            //console.log(val.DOB.$date.$numberLong)
            // Convert $numberLong to JavaScript Date object
            if(val.DOB.$date){
            var date = new Date(parseInt(val.DOB.$date.$numberLong));

             // Format the date as a string (e.g., "YYYY-MM-DD HH:mm:ss")
            //var formattedDate = date.toISOString().slice(0, 19).replace("T", " ");
            //console.log(formattedDate)
            //val.DOB=formattedDate
            }
            //app.customer = val;
            //console.log('API Response:', app.customer);
            //this.isEditing=false;
            console.log(val)
            return val;
          })
          .catch((error) => {
            console.error('Error fetching customer data:', error);
          });
}

 function offerSave2(offer){
            //if (offerID ==""){
            console.log(offer)
            console.log(app.offer)
             axios.post('http://localhost:5000/jso/saveOfferDetails',{data:offer}).then((response) => {
            //console.log('API Response:', JSON.parse(response));
            //this.customer = JSON.parse(response.data.CustomerDetails);
            this.isEditing=false;
          })
          .catch((error) => {
            console.error('Error fetching customer data:', error);
          });
        }
 function auditTrailSummary(){
             axios.post('http://localhost:5000/jso/DeployNoActionOrMidwayMail',{type: "midway",inputs : "Offer Status :  "+offerDetails.StatusText +", LastModified : "+offerDetails.LastModified.$date + ", CreatedOn : "+offerDetails.CreatedOn.$date+ ", ValidityInDays : "+offerDetails.ValidityInDays  }).then((response) => {
                 });
        }
 function NoActionMidWayReminder(){
         axios.post('http://localhost:5000/jso/getOfferStatus',{id: offerID}).then((response) => {
             console.log(response)
            //compare the Dates
            console.log(JSON.parse(response.data.offerDetails).Status)
            offerDetails = JSON.parse(response.data.offerDetails)
            if(offerDetails.Status < 80 && offerDetails.Status > 20){
                alert("This offer left mid-way by the customer. \n \n  Please find the offer Details below,\n Offer Status :  "+offerDetails.StatusText +", \n LastModified : "+offerDetails.LastModified.$date + ", \n CreatedOn : "+offerDetails.CreatedOn.$date+ ", \n ValidityInDays : "+offerDetails.ValidityInDays + "\n \n Please check your email for the sample Email")
                 axios.post('http://localhost:5000/jso/DeployNoActionOrMidwayMail',{type: "midway",inputs : "Offer Status :  "+offerDetails.StatusText +", LastModified : "+offerDetails.LastModified.$date + ", CreatedOn : "+offerDetails.CreatedOn.$date+ ", ValidityInDays : "+offerDetails.ValidityInDays  }).then((response) => {
                 });
            }
             if(offerDetails.Status < 30){
                alert("No action on this offer by the customer. \n \n Please find the offer Details below,\n Offer Status :  "+offerDetails.StatusText +", \n LastModified : "+offerDetails.LastModified.$date + ", \n CreatedOn : "+offerDetails.CreatedOn.$date+ ", \n ValidityInDays : "+offerDetails.ValidityInDays + "\n \n Please check your email for the sample Email")
                 axios.post('http://localhost:5000/jso/DeployNoActionOrMidwayMail',{type: "noaction", inputs : "Offer Status :  "+offerDetails.StatusText +", LastModified : "+offerDetails.LastModified.$date + ", CreatedOn : "+offerDetails.CreatedOn.$date+ ", ValidityInDays : "+offerDetails.ValidityInDays}).then((response) => {
                 });
            }
          })
          .catch((error) => {
            console.error('Error fetching customer data:', error);
          });

        }
 function sendOTP(customerID){
            //if (offerID ==""){
             axios.post('http://localhost:5000/jso/sendOTP',{data:this.offer}).then((response) => {
             console.log(response.data.status)
             //console.log('API Response:', JSON.parse(response));
            //this.customer = JSON.parse(response.data.CustomerDetails);
            this.OTPDisp = response.data.status.otp
            this.isEditing=false;
          })
          .catch((error) => {
            console.error('Error fetching customer data:', error);
          });
        }
 function ProceedWithOffer(){
            axios.post('http://localhost:5000/jso/ProceedWithOffer',{"offerID":offerID}).then((response) => {
             console.log(response)
             if (response.data.status == "FAIL"){
              alert("something went wrong!")
             }
             else if  (response.data.status == "Thanks for choosing the offer. You will get a notification soon"){
              alert("Thank you for selecting this offer. You will receive an OTP shortly. Please input the OTP here to continue.");
             }
            this.isEditing=false;
          })
          .catch((error) => {
            console.error('Error fetching customer data:', error);
          });
         }
 function NotInterested(){
            axios.post('http://localhost:5000/jso/NotInterested',{"offerID":offerID}).then((response) => {
             console.log(response)
             if (response.data.status == "FAIL"){
              alert("something went wrong!")
             }
             else if  (response.data.status == "Thanks for your update"){
              alert(response.data.status);
             }
            this.isEditing=false;
          })
          .catch((error) => {
            console.error('Error fetching customer data:', error);
          });
         }
 function OTPLogin2(offer){

            url=window.location.href
            const [hash, query] = url.split('#')[1].split('?')
            const params = Object.fromEntries(new URLSearchParams(query))
            const offerID=params.id
            console.log(offerID,offer.OTP )
             axios.post('http://localhost:5000/jso/OTPlogin',{"otp":offer.OTP,"offerID": offerID}).then((response) => {
             console.log(response)
             if (response.data.status == "FAIL"){
              alert("OTP Validation Failed")
              this.OTPVALIDATION=false;
             }
             else if  (response.data.status == "PASS"){
              alert("OTP verified. You will get the email shortly with more details.");
              this.OTPVALIDATION=true;
             }
            this.isEditing=false;
          })
          .catch((error) => {
            console.error('Error fetching customer data:', error);
          });
        }


     // Get the hash portion of the URL
        var hash = window.location.hash;
      //alert('before mount')
      const app = Vue.createApp({

        data() {
        return {
          customers: [{"First_Name":"Tome"},{"First_Name":"Jomme"}],
           offers: [],
           customer: [],
           audittrails: [],
           camreports: [],
           offer: {"Type":"Loan"
          ,"Status":"New",
          "Account_ID":"23243",
          "Amount":1000,
          "OTP":111111,
          "customerDetails":{
          "First_Name":"adad",
          "Last_Name":"kat",
          "Address": "",
          "Account_ID": "",
          "Age":0
          }
          },
          showCustDetails:false,
          showCustomers:true,
          isEditing:false,
          showOffers:false,
          showAudits:false,
          showCams:false,
          showOfferDetails:false

        }
        },
        delimiters : ['[[', ']]'],
      mounted() {
        const app = this;

              // Define a function to handle hash changes
        function handleHashChange() {
  // Get the new hash value
  var hash = window.location.hash;
  hashsplit=hash.split("?")
  if (hashsplit.length>0)
  hash=hashsplit[0]
  else
  hash=hash

  // Your code here to handle the hash change
   console.log("Hash changed to: " + hash);

      // Check if the hash is not empty and contains the text "Login"
        if (hash !== "" && hash === "#customer-section") {
           app.showCustomers = true;
           app.showCustDetails = false;
           axios.get('http://localhost:5000/jso/getCustomers') // Replace with your API endpoint URL
          .then((response) => {
            console.log('API Response:', JSON.parse(response.data.customers));
            app.customers = JSON.parse(response.data.customers);
          })
          .catch((error) => {
            console.error('Error fetching customer data:', error);
          });
        }
        else if ( hash === "#customerDetails-Section") {
             app.showCustomers = false;
           app.showCustDetails = true;
           app.offerDetails=true
            console.log("Hash changed to: " + hash);
            getCustomerDetails()
              .then(data => {
                // Handle the data returned from the fetchData function
                console.log('Data:', data);
                app.customer=data;
              })
              .catch(error => {
                // Handle any errors that occurred during the fetchData function
                console.error('Error:', error);
              });
        }
        else if ( hash === "#offer-Section") {
          app.showOffers=true;
          app.showAudits=false;
          app.showCams=false;
          app.showCustDetails=false,
          app.showCustomers=false,
          app.isEditing=false
          app.offerDetails=true
           axios.get('http://localhost:5000/jso/getOffers') // Replace with your API endpoint URL
          .then((response) => {
            console.log('API Response:', JSON.parse(response.data.offers));
            app.offers = JSON.parse(response.data.offers);
          })
          .catch((error) => {
            console.error('Error fetching customer data:', error);
          });
        }
         else if ( hash === "#audit-section") {
          app.showOffers=false;
          app.showAudits=true;
          app.showCams=false;
           app.showCustDetails=false,
          app.showCustomers=false,
          app.isEditing=false,
          app.offerDetails=true
          axios.get('http://localhost:5000/jso/getAudittrails')
          .then((response) => {
            console.log('API Response:', JSON.parse(response.data.audittrails));
            app.audittrails = JSON.parse(response.data.audittrails);
          })
          .catch((error) => {
            console.error('Error fetching customer data:', error);
          });
        }
         else if ( hash === "#cam-section") {
          app.showOffers=false;
          app.showAudits=false;
          app.showCams=true;
           app.showCustDetails=false;
          app.showCustomers=false;
          app.isEditing=false;
          app.offerDetails=true;
          axios.get('http://localhost:5000/jso/getCAMReports')
          .then((response) => {
            console.log('API Response:', JSON.parse(response.data.camreports));
            app.camreports = JSON.parse(response.data.camreports);
          })
          .catch((error) => {
            console.error('Error fetching customer data:', error);
          });
        }

         else if ( hash === "#offerDetails-Section") {
          //const urlParams = new URLSearchParams(window.location.search);
          //const offerID = urlParams.get('id');
          url=window.location.href
          const [hash, query] = url.split('#')[1].split('?')
          const params = Object.fromEntries(new URLSearchParams(query))
          const offerID=params.id
          app.showOffers=false;
          app.showAudits=false;
          app.showCams=false;
           app.showCustDetails=false;
          app.showCustomers=false;
          app.isEditing=false;
          app.showOfferDetails=true;
           if (offerID != null){
        axios.post('http://localhost:5000/jso/getOfferDetails',{id: offerID}).then((response) => {
            //console.log('API Response:', JSON.parse(response));
            if(response.data.OfferDetails){
            }
            //console.log(response.data.OfferDetails.OTP)
           // console.log(response.data.OfferDetails)

            app.offer = JSON.parse(response.data.OfferDetails);
            app.OTPDisp =  app.offer.OTP
            app.offer.OTP=""
            app.Role=response.data.Role
            console.log(app.offer)
            //console.log(this.offer.customerDetails.First_Name)
            app.isEditing=false;
            if (app.offer.OTPDisp !=""){
               app.OTPSend = 1
               }
          })
          .catch((error) => {
            console.error('Error fetching customer data:', error);
          });
          }
      }


}


        // Add an event listener for the hashchange event
        window.addEventListener("hashchange", handleHashChange);


      },
      methods:{
       offerSave1(){
       console.log(this.offer)
          offerSave2(this.offer)

       },
       OTPLogin1(){
       OTPLogin2(this.offer)
       },
        openDetails(customerID){
               //console.log(customerID)
               this.showCustomers = false;
               this.showCustDetails = true;
               idObj=customerID;

               console.log(idObj.$oid)
               //window.location.href="/customerDetails?id="+customerID.$oid
              window.location.hash = "#customerDetails-Section?id="+customerID.$oid;
        },
        openOfferDetails(offerID){
               //console.log(customerID)
               //idObj=customerID;
               //console.log(idObj);
               //console.log(customerID.$oid)
               //console.log(idObj.$oid)
               //window.location.href="/offerDetails?id="+offerID.$oid
                window.location.hash = "#offerDetails-Section?id="+offerID.$oid;
        },
        extractOid(idObj) {
      if (idObj && idObj["$oid"]) {
        return idObj["$oid"];
      }
      return "";
        },
        editSave(customerID){
             //console.log(customerID);
             console.log(this.customer);
             axios.post('http://localhost:5000/jso/saveCustomerDetails',{data:this.customer}).then((response) => {
            //console.log('API Response:', JSON.parse(response));
            //this.customer = JSON.parse(response.data.CustomerDetails);
            this.isEditing=false;
          })
          .catch((error) => {
            console.error('Error fetching customer data:', error);
          });
        },
        sendOffer(){
             axios.post('http://localhost:5000/jso/sendOffer',{data:this.customer}).then((response) => {
            this.isEditing=false;
          })
          .catch((error) => {
            console.error('Error fetching customer data:', error);
          });
        }
      }
    });
    // Mount the Vue app to the element with id "app"
    app.mount('#CustomersView');