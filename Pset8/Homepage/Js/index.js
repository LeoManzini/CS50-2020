function greet()
{
    let name = document.querySelector('#name').value;
    if (name != '')
    {
        alert('Thanks Mr(s) ' + name + ' your Feedback was sent!');
        document.location.reload(true);
    }
    else
    {
        name = 'anonymous person';
        alert('Thanks Mr(s) ' + name + ' your Feedback was sent!');
        document.location.reload(true);
    }
}