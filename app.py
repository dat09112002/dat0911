from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'  
db = SQLAlchemy(app)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text, nullable=False)

# Flask route to handle form submission for reviews
@app.route('/submit_review', methods=['POST'])
def submit_review():
    username = request.form['username']
    rating_value = int(request.form['rating'])
    review_text = request.form['review']
    product_id = int(request.form['product_id'])
    product_name = request.form['product_name']
    
    # Create a Review object and add it to the database
    review = Review(username=username, product_id=product_id, rating=rating_value, review=review_text)
    db.session.add(review)
    db.session.commit()

    # Redirect to the review page for the specific product
    return redirect(url_for('review', product_id=product_id, product_name=product_name))

# Flask route to display the review page for a specific product
@app.route('/review/<int:product_id>/<product_name>')
def review(product_id, product_name):
    # Fetch reviews for the specific product_id
    reviews = Review.query.filter_by(product_id=product_id).all()

    return render_template('review.html', product_id=product_id, product_name=product_name, reviews=reviews)

@app.route('/')
def main():
    # Fetch reviews for each product (adjust as needed)
    reviews_product1 = Review.query.filter_by(product_id=1).all()
    reviews_product2 = Review.query.filter_by(product_id=2).all()
    reviews_product3 = Review.query.filter_by(product_id=3).all()

    return render_template('main.html', reviews_product1=reviews_product1, reviews_product2=reviews_product2, reviews_product3=reviews_product3)

@app.route('/allreviews')
def all_reviews():
    # Fetch all reviews
    all_reviews = Review.query.all()

    return render_template('allreviews.html', all_reviews=all_reviews)


@app.route('/edit_review/<int:review_id>', methods=['POST'])
def edit_review(review_id):
    # Assuming you have a function to retrieve a review by its ID
    review = Review.query.get(review_id)
    
    if review:
        # Update review text based on the form data
        edited_review = request.form['edit_review']
        review.review_text = edited_review
        db.session.commit()
        flash('Review edited successfully!', 'success')
    else:
        flash('Review not found!', 'error')

    return redirect(url_for('review', product_id=product_id, product_name=product_name))

# Update your existing delete_review route to accept POST requests
@app.route('/delete_review/<int:rating>', methods=['POST'])
def delete_review(rating):
    # Assuming you want to delete reviews with a specific rating
    reviews_to_delete = Review.query.filter_by(rating=rating).all()

    # Delete each review
    for review in reviews_to_delete:
        db.session.delete(review)

    # Commit changes to the database
    db.session.commit()

    return redirect(url_for('all_reviews'))


# Flask route to display the page for editing a specific review
@app.route('/edit_review_page/<int:review_id>')
def edit_review_page(review_id):
    # Fetch the review by its ID
    review = Review.query.get(review_id)

    # Render the HTML page for editing the review
    return render_template('edit_review.html', review=review)


@app.route('/product1')
def product1():
    return render_template('product1.html')

@app.route('/product2')
def product2():
    return render_template('product2.html')

@app.route('/product3')
def product3():
    return render_template('product3.html')




with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, port=4700)
