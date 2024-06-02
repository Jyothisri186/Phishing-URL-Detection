#importing required libraries

from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
warnings.filterwarnings('ignore')
from feature import FeatureExtraction

file = open("pickle/model.pkl","rb")
gbc = pickle.load(file)
file.close()


app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30)
        y_pred = gbc.predict(x)[0]
        y_pro_phishing = gbc.predict_proba(x)[0,0]
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]

        if y_pred == -1:
            # If predicted as phishing, gather feature names
            feature_names = []
            features = obj.getFeaturesList()
            feature_names = [
                "UsingIP: URL contains an IP address, which is often associated with phishing attempts",
                "LongURL: URL that exceeds a certain length, typically considered less user-friendly",
                "ShortURL: A condensed version of a URL, often used for sharing links and saving space",
                "Symbol@: Presence of the @ symbol in a URL, commonly used in email addresses",
                "Redirecting//: Indication of URL redirection using forward slashes",
                "PrefixSuffix-: Addition of prefixes or suffixes to a domain name",
                "SubDomains: Subsections or subdivisions within a domain",
                "HTTPS: Secure version of HTTP, ensuring encrypted communication between a user's browser and the website",
                "DomainRegLen: Length of time a domain has been registered",
                "Favicon: Small icon associated with a website, typically displayed in the browser's address bar or next to the site's name in bookmarks",
                "NonStdPort: Use of a non-standard port for accessing a website",
                "HTTPSDomainURL: Presence of HTTPS in the domain URL, indicating a secure connection",
                "RequestURL: URL used to request resources from a server",
                "AnchorURL: URL linked to by an anchor tag within a webpage",
                "LinksInScriptTags: Links embedded within script tags in HTML",
                "ServerFormHandler: Server-side processing of form data submitted by users",
                "InfoEmail: Email address provided for inquiries or information on the website",
                "AbnormalURL: URL exhibiting unusual or suspicious characteristics",
                "WebsiteForwarding: Automatic redirection of a website to another URL",
                "StatusBarCust: Customization of the browser's status bar",
                "DisableRightClick: Prevention of right-clicking on a webpage, often to protect content",
                "UsingPopupWindow: Displaying content or advertisements in popup windows",
                "IframeRedirection: Redirection of content within an iframe element",
                "AgeofDomain: Age of a domain since its registration",
                "DNSRecording: Record of domain name system (DNS) information",
                "WebsiteTraffic: Amount of visitors or users accessing a website",
                "PageRank: Algorithm used by Google to rank web pages in search results",
                "GoogleIndex: Inclusion of a webpage in Google's search index",
                "LinksPointingToPage: Number of external links directed towards a webpage",
                "StatsReport: Report containing various statistics related to a website",
            ]
            
            phishing_features = [feature_names[i] for i in range(len(features)) if features[i] == -1]

            # Render template with feature names for phishing websites
            return render_template('index.html', xx=round(y_pro_non_phishing, 2), url=url, features=phishing_features)
        else:
            # Render template without feature names for safe websites
            return render_template('index.html', xx=round(y_pro_non_phishing, 2), url=url)
    return render_template("index.html", xx=-1)




if __name__ == "__main__":
    app.run(debug=True)