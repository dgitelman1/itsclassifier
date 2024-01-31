const Output = ({ isDev, outputData }) => {
    return (
        <>
            <form className="ui form">
                <textarea
                    id="original_email"
                    type="text"
                    value={outputData}
                />
            </form>
        </>
    );
};

export default Output;