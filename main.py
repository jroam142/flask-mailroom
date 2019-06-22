import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/new-donation', methods=["GET", "POST"])
def new_donation():
    if request.method == "POST":
        input_name = request.form['donor-name']
        donation_amount = int(request.form['donation-amount'])

        try:
            donor = Donor.select().where(Donor.name == input_name).get()
        except:
            donor = Donor(name=input_name)
            donor.save()

        new_donation = Donation(value=donation_amount, donor=donor)
        new_donation.save()

        return redirect(url_for('all'))
    return render_template('new_donation.jinja2')


@app.route('/individual-donations', methods=['GET', 'POST'])
def indiv_donation():
    if request.method == 'POST':
        donor_name = request.form['donor-name']
        if donor_name != 'all':
            try:
                retrieved_donor = Donor.select().where(Donor.name == donor_name).get()
                all_donations = Donation.select().where(Donation.donor == retrieved_donor)

                return render_template('individual_donations.jinja2', donor_name=donor_name, all_donations=all_donations, post=True)
            except:
                return render_template('individual_donations.jinja2', donor_name=donor_name, post=True)

    all_donors = Donor.select()
    return render_template('individual_donations.jinja2', all_donors=all_donors)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

