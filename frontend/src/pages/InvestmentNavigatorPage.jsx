import ChatPageLayout from './ChatPageLayout';
import InvestmentNavigatorChat from '../components/chat/InvestmentNavigatorChat';

const InvestmentNavigatorPage = () => {
  const category = {
    id: 'investment-navigator',
    title: 'Investment Navigator',
    description: 'Discover new investment opportunities'
  };

  return (
    <ChatPageLayout category={category}>
      {(props) => <InvestmentNavigatorChat {...props} />}
    </ChatPageLayout>
  );
};

export default InvestmentNavigatorPage;

