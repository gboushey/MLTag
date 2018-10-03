 <form action="/classify" method="get">
	<p/>
	Classifier:
	<select name='classifier'>
		%for c in classifiers:
			<option>{{c}}</option>
		%end
	</select>
	<p/>
	Classifier Type
	<p/>
	<select name='classifier_type'>
			<option>MultinomialNB</option>
			<option>RandomForest</option>
			<option>LogisticRegression</option>
			<option>MLP</option>
	</select>
	<p/>
    Entry: 
	<p/>
	<textarea rows="20" cols="100" name="text"></textarea>
	<p/>
    <input value="Rate" type="submit" />
</form>
