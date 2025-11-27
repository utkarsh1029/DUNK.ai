import ChatPageLayout from './ChatPageLayout';
import SmartExpenseCoachChat from '../components/chat/SmartExpenseCoachChat';

const SmartExpenseCoachPage = () => {
  const category = {
    id: 'smart-expense-coach',
    title: 'Smart Expense Coach',
    description: 'Get insights on your spending patterns'
  };

  return (
    <ChatPageLayout category={category}>
      {(props) => <SmartExpenseCoachChat {...props} />}
    </ChatPageLayout>
  );
};

export default SmartExpenseCoachPage;

