

const fuzzResultData = [
  {
    id: 1,
    user: 'User 1',
    output: {
      response: 'Response 1',
      lines: 100,
      words: 500,
      chars: 2500,
      timeTaken: '5s',
      payload: 'Payload 1'
    },
    targetUrl: 'http://example.com',
    fuzzType: 'Type 1'
  },
  {
    id: 2,
    user: 'User 2',
    output: {
      response: 'Response 2',
      lines: 120,
      words: 600,
      chars: 3000,
      timeTaken: '6s',
      payload: 'Payload 2'
    },
    targetUrl: 'http://example.org',
    fuzzType: 'Type 2'
  },
  {
    id: 2,
    user: 'User 2',
    output: {
      response: 'Response 2',
      lines: 120,
      words: 600,
      chars: 3000,
      timeTaken: '6s',
      payload: 'Payload 2'
    },
    targetUrl: 'http://example.org',
    fuzzType: 'Type 2'
  },
 

];

const FuzzResultTable = () => {
  return (
    <div className=" bg-gray-800 text-gray-200 p-3 rounded-lg shadow-lg ml-10">
      <table className="min-w-full border-collapse rounded-lg overflow-hidden">
        <thead>
          <tr className="bg-gray-900">
            <th className="py-4 px-2 text-left">S.No.</th>
            <th className="py-4 px-2 text-left">User</th>
            <th className="py-4 px-2 text-left">Response</th>
            <th className="py-4 px-2 text-left">Lines</th>
            <th className="py-4 px-2 text-left">Words</th>
            <th className="py-4 px-2 text-left">Chars</th>
            <th className="py-4 px-2 text-left">Time Taken</th>
            <th className="py-4 px-2 text-left">Payload</th>
            <th className="py-4 px-2 text-left">Target URL</th>
            <th className="py-4 px-2 text-left">Fuzz Type</th>
          </tr>
        </thead>
        <tbody>
          {fuzzResultData.map((item, index) => (
            <tr key={item.id} className="hover:bg-gray-700 transition duration-300 ease-in-out">
              <td className="py-4 px-2">{index + 1}</td>
              <td className="py-4 px-2">{item.user}</td>
              <td className="py-4 px-2">{item.output.response}</td>
              <td className="py-4 px-2">{item.output.lines}</td>
              <td className="py-4 px-2">{item.output.words}</td>
              <td className="py-4 px-2">{item.output.chars}</td>
              <td className="py-4 px-2">{item.output.timeTaken}</td>
              <td className="py-4 px-2">{item.output.payload}</td>
              <td className="py-4 px-2">{item.targetUrl}</td>
              <td className="py-4 px-2">{item.fuzzType}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FuzzResultTable;
