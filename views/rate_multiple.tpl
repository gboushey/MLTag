 <form action="/classify_multiple" method="get">
	<p/>
	Classifier:
	<p/>
	<select multiple size="30" name='classifiers'>
		%for c in classifiers:
			<option>{{c}}</option>
		%end
	</select>
	<p/>
    Entry: 
	<p/>
	<textarea rows="20" cols="100" name="text"></textarea>
	<p/>
    <input value="Rate" type="submit" />
</form>
