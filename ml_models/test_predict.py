# from url_feature_extractor import extract_url_features, batch_extract

# import pandas as pd
# import joblib

# # --- Load model ---
# model = joblib.load("phishguard_xgboost.joblib")

# # --- Sample URLs to test ---
# urls = [
#     "sontemeda.altervista.org/paypinoko/paypinoko/procesing.php",
#     "www.coincoele.com.br/Scripts/smiles/?pt-br/Paginas/default.aspx",
#     "myxxxcollection.com/v1/js/jih321/bpd.com.do/do/l.popular.php",
#     "www.aclaydance.com/ncpf.php",
#     "https://paypal.com.verify-account.fake.com",
#     "www.dghjdgf.com/paypal.co.uk/cycgi-bin/webscrcmd=_home-customer&nav=1/loading.php",
#     "https://www.google.com",
#     "https://www.wikipedia.org",
#     "https://www.amazon.com",
#     "https://www.microsoft.com",
    
# ]

# # --- Extract features ---
# features_df = batch_extract(urls)

# # --- Predict ---
# probs = model.predict_proba(features_df)[:, 1]
# preds = model.predict(features_df)

# # --- Print Results ---
# for url, pred, prob in zip(urls, preds, probs):
#     label = "Phishing" if pred == 1 else "Safe"
#     print(f"[URL] {url}\n -> Prediction: {label} (Confidence: {prob:.2f})\n")

from url_feature_extractor import batch_extract
import joblib
import pandas as pd

# --- Load models ---
models = {
    "Logistic Regression": joblib.load("phishguard_logreg.joblib"),
    "Random Forest": joblib.load("phishguard_rf.joblib"),
    "XGBoost": joblib.load("phishguard_xgboost.joblib"),
}

# --- Sample URLs to test ---
urls = [
    "sontemeda.altervista.org/paypinoko/paypinoko/procesing.php",
    "www.coincoele.com.br/Scripts/smiles/?pt-br/Paginas/default.aspx",
    "www.aclaydance.com/ncpf.php",
    "https://paypal.com.verify-account.fake.com",
    "www.dghjdgf.com/paypal.co.uk/cycgi-bin/webscrcmd=_home-customer&nav=1/loading.php",
    "https://www.google.com",
    "https://www.wikipedia.org",
    "https://www.amazon.com",
    "https://www.microsoft.com",
    "https://www.google.com",
    "https://mail.google.com",
    "https://docs.google.com",
    "https://drive.google.com",
    "https://www.microsoft.com",
    "https://login.microsoftonline.com",
    "https://outlook.office.com",
    "https://www.facebook.com",
    "https://m.facebook.com",
    "https://developers.facebook.com",
    "https://www.apple.com",
    "https://support.apple.com",
    "https://www.amazon.com",
    "https://aws.amazon.com",
    "https://www.netflix.com",
    "https://accounts.spotify.com",
    "https://www.linkedin.com",
    "https://www.researchgate.net",
    "https://www.dropbox.com",
    "https://www.paypal.com"

]

# --- Extract features ---
features_df = batch_extract(urls)

# --- Collect results ---
results = []

for url in urls:
    row = {"URL": url}
    feats = features_df.loc[[urls.index(url)]]  # extract features for this URL
    for name, model in models.items():
        prob = model.predict_proba(feats)[:, 1][0]
        pred = "Phishing" if prob >= 0.5 else "Safe"
        row[name] = f"{pred} ({prob:.2f})"
    results.append(row)

# --- Display as table ---
df_results = pd.DataFrame(results)
print("\n=== Model Comparison Results ===\n")
print(df_results.to_string(index=False))
