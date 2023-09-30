
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
          showCustDetails:false,
          showCustomers:true,
          isEditing:false,
          showOffers:false,
          showAudits:false,
          showCams:false,

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
             this.showCustomers = false;
           this.showCustDetails = true;
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
          app.isEditing=false
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
           app.showCustDetails=false,
          app.showCustomers=false,
          app.isEditing=false
          axios.get('http://localhost:5000/jso/getCAMReports')
          .then((response) => {
            console.log('API Response:', JSON.parse(response.data.camreports));
            this.camreports = JSON.parse(response.data.camreports);
          })
          .catch((error) => {
            console.error('Error fetching customer data:', error);
          });
        }



}


        // Add an event listener for the hashchange event
        window.addEventListener("hashchange", handleHashChange);


      },
      methods:{
        openDetails(customerID){
               //console.log(customerID)
               this.showCustomers = false;
               this.showCustDetails = true;
               idObj=customerID;
               //console.log(idObj);
               //console.log(customerID.$oid)
               console.log(idObj.$oid)
               //window.location.href="/customerDetails?id="+customerID.$oid
              window.location.hash = "#customerDetails-Section?id="+customerID.$oid;
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